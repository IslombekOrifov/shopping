from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import OuterRef, Sum, Avg, F

from common.services import get_price_like_float
from .models import WishedProduct
from accounts.models import CustomUser
from products.models import Product, ProductItem, ProductImage
from general.models import Currency
from general.services import get_currency_from_session



def wishlist_add(request, slug):
    user = request.user
    product = get_object_or_404(ProductItem, slug=slug, is_active=True, is_archive=False, is_deleted=False)
    if user.is_authenticated and user.role == CustomUser.CHOICE_ROLE[0][0]:
        if WishedProduct.objects.filter(client=user, product=product).exists():
            pass
        else:
            WishedProduct.objects.create(client=user, product=product)
        return redirect('wishlists:detail')
        # return HttpResponse('done')
    elif user.is_anonymous:
        wishlist = request.session.get(settings.WISHLIST_SESSION_ID)
        if not wishlist:
            wishlist = request.session[settings.WISHLIST_SESSION_ID] = {}
        product_id = str(product.id)
        if product_id not in wishlist:
            wishlist[product_id] = 'True'
            request.session.modified = True
            return HttpResponse('done')
        return HttpResponse('exact')
    else:
        return HttpResponse("Sizga wishlist qo'shish mumkin emas")
    

def wishlist_detail(request):
    currency_price = Currency.objects.get(code=get_currency_from_session(request)).price
    user = request.user
    if user.is_authenticated and user.role == CustomUser.CHOICE_ROLE[0][0]:
        product_ids = WishedProduct.objects.values_list()
        product_items = ProductItem.objects.filter(is_deleted=False, is_archive=False,
            wishlists__client=user).annotate(price_currency=get_price_like_float('price') / currency_price, 
            image=ProductImage.objects.filter(product_item=OuterRef('pk')
            ).values('image_middle')[:1]).order_by('-wishlists__created')
        return render(request, 'wishlists/wishlist.html', {'product_items': product_items})
    elif user.is_anonymous:
        wishlist = request.session.get(settings.WISHLIST_SESSION_ID)
        if not wishlist:
            product_items = None
        else:
            product_ids = [int(key) for key, value in request.session[settings.WISHLIST_SESSION_ID].items()]
            product_items = ProductItem.objects.filter(is_deleted=False, is_active=True, is_archive=False,
            count_in_stock__gt=0, id__in=product_ids).annotate(price_currency=get_price_like_float('price') / currency_price,
            image=ProductImage.objects.filter(product_item=OuterRef('pk')).values('image_middle')[:1]).order_by('-created')
        return render(request, 'wishlists/wishlist.html', {'product_items': product_items})
    else:
        return HttpResponse("Sizga wishlist qo'shish mumkin emas")


def wishlist_remove(request, id):
    user = request.user
    if user.is_authenticated and user.role == CustomUser.CHOICE_ROLE[0][0]:
        WishedProduct.objects.filter(client=user, product__id=id).delete()
        return redirect('wishlists:detail')
    elif user.is_anonymous:
        if str(id) in request.session[settings.WISHLIST_SESSION_ID]:
            del request.session[settings.WISHLIST_SESSION_ID][str(id)]
        return redirect('wishlists:detail')
    else:
        return HttpResponse("Sizga wishlist qo'shish mumkin emas")
