from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from decimal import Decimal, ROUND_UP
import json

from .models import Order, OrderItem
from .forms import OrderAddressForm
from carts.cart import Cart
from general.models import Currency
from discounts.models import DiscountItem
from general.models import Currency
from general.services import get_currency_from_session
from common.services import get_price_like_float


from payme.receipts.subscribe_receipts import PaymeSubscribeReceipts
from pprint import pprint


@login_required
def order_checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        forms = OrderAddressForm(request.POST)
        if forms.is_valid():
            if forms.cleaned_data['terms'] == True:
                currency_price = Currency.objects.get(code='USD').price
                user = request.user
                cd = forms.cleaned_data
                adres = f"Shahar/viloyat: {cd['senderRegion']}, tuman: {cd['senderCity']}, address: {cd['address']}, home number:{cd['home_number']}, postal code: {cd['postal_code']}"
                order = Order.objects.create(
                    desc=cd['order_desc'], client=user, total_price=cart.get_total_price(),
                    total_price_in_usd=cart.get_total_price_in_usd(),
                    address=adres, phone=cd['phone'], terms=True
                )
                for item in cart:
                    price_usd = Decimal((item['price'] / currency_price).quantize(Decimal('.01'), rounding=ROUND_UP))
                    if item.get('price_discount'):
                        disc = DiscountItem.objects.filter(product_item=item['item'], is_active=True)[:1].get()
                        disc.booked=item['quantity']
                        disc.save()
                        OrderItem.objects.create(
                            product_item=item['item'], order=order, quantity=item['quantity'], price=item['price'],
                            discount_price=item['price_discount'], price_in_usd=price_usd, currency_course=currency_price 
                        )
                    else:
                        OrderItem.objects.create(
                            product_item=item['item'], order=order, quantity=item['quantity'],
                            price=item['price'], price_in_usd=price_usd, currency_course=currency_price   
                        )
                rclient = PaymeSubscribeReceipts(
                    base_url="https://checkout.test.paycom.uz/api/",
                    paycom_id="5e730e8e0b852a417aa49ceb",
                    paycom_key="#MWnwHNYATJo%W@XvO5nISiY&mG7PEuzDX18"
                )
                
                resp = rclient._receipts_create(
                    amount=int(order.total_price),
                    order_id=f"{order.id}"
                )
                

                pprint(resp)
                # jsdata = json.loads(resp)
                order.transaction_code = resp['result']['receipt']['_id']
                order.save()

                cart.clear()
                request.session['order_id'] = order.id
                # return redirect(reverse('payment:process'))
                return redirect(reverse('payment:payme_process'))
                # return render(request, 'orders/created.html', {'order': order})
    else:
        forms = OrderAddressForm()
    return render(request, 'orders/checkout.html', {'cart': cart, 'forms': forms})


@login_required
def order_delete(request, slug, page=None):
    order = Order.objects.get(slug=slug)
    order.delete()
    return redirect('accounts:orders')



def order_details(request, slug):
    currency_price = Currency.objects.get(code=get_currency_from_session(request)).price

    order = Order.objects.filter(slug=slug, client=request.user).annotate(
        price_currency=get_price_like_float('total_price') / currency_price,
    ).prefetch_related('items').get()
    context = {
        'order': order,
        'section': 'orders'
    }
    return render(request, 'orders/details.html', context)