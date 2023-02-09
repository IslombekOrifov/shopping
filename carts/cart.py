from decimal import Decimal, ROUND_UP
import decimal
from django.conf import settings
from django.db.models import OuterRef, F, Func
from django.utils import timezone

from products.models import Product, ProductItem, ProductImage
from general.models import Currency
from general.services import get_currency_from_session
from discounts.models import DiscountItem
from discounts.services import get_discount_by_product_item


class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] =  {}
        self.cart = cart


    def add(self, product_item, quantity=1, update_quantity=False):
        item_id = str(product_item.id)
        discount = get_discount_by_product_item(product_item)
        if not discount:
            if item_id not in self.cart:
                self.cart[item_id] = {'quantity': 0, 'price': str(product_item.price), 'adding_time': timezone.now().timestamp()}
            if update_quantity:
                self.cart[item_id]['quantity'] = quantity
                self.cart[item_id]['adding_time'] = timezone.now().timestamp()
            else:
                self.cart[item_id]['quantity'] += quantity
        else:
            item_id = str(product_item.id) + '+' + 'discount'
            if item_id not in self.cart:
                self.cart[item_id] = {'quantity': 0, 'price': str(product_item.price), 
                    'adding_time': timezone.now().timestamp(), 'price_discount': str(discount[0].price)
                }
            if update_quantity:
                self.cart[item_id]['quantity'] = quantity
                self.cart[item_id]['adding_time'] = timezone.now().timestamp()
            else:
                self.cart[item_id]['quantity'] += quantity
        self.save()
    

    def save(self):
        self.session.modified = True

    
    def remove(self, card_id):
        del self.cart[card_id]
        self.save()


    def __iter__(self):
        currency_price = Currency.objects.get(code=get_currency_from_session(self.request)).price
        items_ids = self.cart.keys()
        cart_and_prod_id_dict = {}
        prod_id_list = []
        for cart_key in items_ids:
            prod_id = cart_key.split('+')
            prod_id_list.append(int(prod_id[0]))
            cart_and_prod_id_dict[cart_key] = int(prod_id[0])
        product_items = ProductItem.objects.filter(is_deleted=False, id__in=prod_id_list).annotate(
            price_currency=(F('price') / currency_price),
            price_discount=Func(DiscountItem.objects.filter(product_item=OuterRef('pk'), 
                quantity__gt=F('sold_quantity'), is_active=True).values('price')[:1], function='CAST', 
                template = '%(function)s(%(expressions)s AS FLOAT)') / currency_price,
            image=ProductImage.objects.filter(product_item=OuterRef('pk') ).values('image_middle')[:1])
        cart = self.cart.copy()
        for key, value in cart_and_prod_id_dict.items():
            product = product_items.get(id=value)
            cart[key]['item'] = product
            cart[key]['key'] = key
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['price_currency'] = Decimal((item['price'] / currency_price).quantize(Decimal('.01'), rounding=ROUND_UP))
            if item.get('price_discount'):
                item['price_discount'] = Decimal(item['price_discount'])
                item['price_discount1'] = Decimal((item['price_discount'] / currency_price).quantize(Decimal('.01'), rounding=ROUND_UP))
                item['total_price'] = item['price_discount1'] * item['quantity']
            else:
                item['total_price'] = (item['price'] * item['quantity'] / currency_price ).quantize(Decimal('.01'), rounding=ROUND_UP)
            yield item


    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    
    def get_total_price(self):
        currency_price = Currency.objects.get(code=get_currency_from_session(self.request)).price
        total = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values()) / currency_price
        return total.quantize(Decimal('.01'), rounding=ROUND_UP)
    
    def get_total_price_in_usd(self):
        currency_price = Currency.objects.get(code='USD').price
        total = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values()) / currency_price
        return total.quantize(Decimal('.01'), rounding=ROUND_UP)


    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()