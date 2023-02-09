from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .cart import Cart
from .forms import CartAddProductForm
from products.models import Product, ProductItem


def cart_add(request, item_id, slug=None):
    cart = Cart(request)
    product_item = get_object_or_404(ProductItem, id=int(item_id))
    if not slug:
        cart.add(product_item=product_item)
        return redirect('carts:cart_detail')
    else:
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product_item=product_item, quantity=cd['quantity'], update_quantity=cd['update'])
        return redirect('carts:cart_detail')



def cart_remove(request, item_id):
    cart = Cart(request)
    product_item = get_object_or_404(ProductItem, id=item_id)
    cart.remove(item_id)
    return redirect('carts:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        print(item)
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'carts/details.html', {'cart': cart})