from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.db.models import Count, Sum, OuterRef, Q, Avg, F, Func
from django.db.models.functions import JSONObject
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from decimal import Decimal, ROUND_UP
import time


from common.decorators import is_ajax, ajax_required
from common.services import get_price_like_float

from carts.forms import CartAddProductForm
from accounts.models import CustomUser

from general.models import Currency
from general.services import get_currency_from_session

from discounts.models import DiscountItem

from .models import *
from .forms import *
from .services import s_order_list




def product_list_seller(request):
    if request.user.role != CustomUser.CHOICE_ROLE[0][0] and  request.user.role != CustomUser.CHOICE_ROLE[-1][0]:
        if Product.objects.filter(company=request.user.company, is_deleted=False):
            products = Product.objects.filter(company=request.user.company, is_deleted=False).annotate(items_count=Count('items')).order_by('-updated')
            return render(request, 'products/product_list_seller.html', {'products': products})
        else:
            return render(request, 'products/product_list_seller.html')
    else:
        raise Http404


def product_detail_seller(request, slug):
    if request.user.role != CustomUser.CHOICE_ROLE[0][0] and  request.user.role != CustomUser.CHOICE_ROLE[-1][0]:
        try:
            product = get_object_or_404(Product, slug=slug, company=request.user.company)
        except:
            product = None
        if product:
            product_items = product.items.filter(is_deleted=False).annotate(images_all=Count('images'))
            return render(request, 'products/product_details.html', {'product': product, 'product_items': product_items})
        else:
            raise Http404
    else:
        raise Http404

# product
def product_create(request):
    if request.method == "POST":
        if request.user.company:
            form = ProductForm(request.POST)
            if form.is_valid():
                product = form.save(commit=False)
                product.author = request.user
                product.who_updated = request.user
                product.company = request.user.company
                product.save()
                messages.success(request, "Product muvaffaqiyatli yaratildi!")
                return HttpResponse("Product muvaffaqiyatli yaratildi!")
            else:
                messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
        else:
            raise Http404
    else:
        form = ProductForm()
    context = {
        'form': form,
    }
    return render(request, 'products/product_create.html', context)


def product_update(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_staff or product.company == request.user.company:
        if request.method == "POST":
            # if product.company == user.company or request.user.is_staff:
            form = ProductForm(instance=product, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Product muvaffaqiyatli yangilandi")
                return HttpResponse("Product muvaffaqiyatli yangilandi!")
            else:
                messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
        else:
            form = ProductForm(instance=product)
        context = {
            'form': form,
        }
        return render(request, 'product/forall/product_update.html', context)
    else:
        messages.error(request, "Siz bu product ni o'zgartira olmaysiz!")
        return redirect("account:dashboard")


def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product.delete()
    return redirect('product_list')
# end product
# ProductItem and ProductImage
def product_item_create(request, slug):
    if request.method == "POST":
        item_form = ProductItemForm(request.POST)
        image_form = ProductImageForm(data=request.POST, files=request.FILES)
        if item_form.is_valid() and image_form.is_valid():
            product = get_object_or_404(Product, slug=slug)
            item = item_form.save(commit=False)
            item.author = request.user
            item.who_updated = request.user
            item.product = product
            item.save()
            images = request.POST.getlist('image_original')
            for img in images:
                ProductImage.objects.create(
                    product_item=item, image_original=img, image_detail=img, 
                    image_big=img, image_middle=img, image_presmall=img, 
                    image_small=img, image_for_cart=img
                )
            messages.success(request, "Produktni itemlari muvaffaqiyatli yaratildi!")
            return HttpResponse("Produktni itemlari muvaffaqiyatli yaratildi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        item_form = ProductItemForm()
        image_form = ProductImageForm()
    context = {
        'item_form': item_form,
        'image_form': image_form,
    }
    return render(request, 'products/product_item_create.html', context)


def product_item_update(request, id):
    item = get_object_or_404(ProductItem, id=id)
    if request.method == "POST":
        item_form = ProductItemForm(instance=item, data=request.POST)
        image_form = ProductImageForm(data=request.POST, files=request.FILES)
        if item_form.is_valid() and image_form.is_valid():
            item_form.save()
            images = request.POST.getlist('image_original')
            if images:
                ProductImage.objects.filter(product_item=item).delete()
                for img in images:
                    ProductImage.objects.create(
                    product_item=item, image_original=img, image_detail=img, 
                    image_big=img, image_middle=img, image_presmall=img, 
                    image_small=img, image_for_cart=img
                )
            messages.success(request, "Produktni itemlari muvaffaqiyatli yangilandi")
            return HttpResponse("Produktni itemlari muvaffaqiyatli yangilandi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        item_form = ProductItemForm(instance=item)
        image_form =ProductImageForm()
        product_images = ProductImage.objects.filter(product_item=item)
    context = {
        'item_form': item_form,
        'image_form': image_form,
        'product_images': product_images,
    }
    return render(request, 'product/foradmin/color_update.html', context)


def product_item_pre_delete(request, id):
    item = get_object_or_404(ProductItem, id=id)
    item.delete = True
    item.save()
    return redirect('product_list')


# category
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kategoriya muvaffaqiyatli yaratildi!")
            return HttpResponse("Categoriya muvaffaqiyatli yaratildi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'product/foradmin/category_create.html', context)


def category_update(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == "POST":
        form = CategoryForm(instance=category, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kategoriya muvaffaqiyatli yangilandi")
            return HttpResponse("Kategoriya muvaffaqiyatli yangilandi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
    }
    return render(request, 'product/foradmin/category_update.html', context)


def category_delete(request, slug):
    category = get_object_or_404(Category, slug=slug)
    category.delete()
    return redirect('category_list')
# end Category
# Brand
def brand_create(request):
    if request.method == "POST":
        form = BrandForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            brand = form.save(commit=False)
            brand.user = request.user
            brand.company = request.user.profile__company
            brand.save()
            messages.success(request, "Brand muvaffaqiyatli yaratildi!")
            return HttpResponse("Brand muvaffaqiyatli yaratildi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = BrandForm()
    context = {
        'form': form,
    }
    return render(request, 'product/forall/brand_create.html', context)


def brand_update(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    if request.user.is_staff or brand.company == request.user.profile__company:
        if request.method == "POST":
            form = BrandForm(instance=brand, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Brand muvaffaqiyatli yangilandi")
                return HttpResponse("Brand muvaffaqiyatli yangilandi!")
            else:
                messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
        else:
            form = BrandForm(instance=brand)
        context = {
            'form': form,
        }
        return render(request, 'product/forall/brand_update.html', context)
    else:
        messages.error(request, "Siz bu brand ni o'zgartira olmaysiz!")
        return redirect("account:dashboard")

def brand_delete(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    brand.delete()
    return redirect('brand_list')
# end brand


def procuct_item_delete(request, id):
    item = get_object_or_404(ProductItem, id=id)
    ProductImage.objects.filter(product_item=item).delete()
    item.delete()
    return redirect('product_list')
# end ProductItem and ProductImage
# ProductRating
def product_rating(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        form = ProductRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.product = product
            rating.user = request.user
            rating.save()
            messages.success(request, "Product rating muvaffaqiyatli yaratildi!")
            return HttpResponse("Product rating muvaffaqiyatli yaratildi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = ProductRatingForm()
    context = {
        'form': form,
    }
    return render(request, 'product/foradmin/color_create.html', context)
# end ProductRating
# ProductComment
def productColor_create(request, slug, id=None):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        form = ProductCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            if id:
                prod_comment = get_object_or_404(ProductComment, pk=id)
                comment.parent = prod_comment
            comment.save()
            messages.success(request, "Product kommentariyasi muvaffaqiyatli yaratildi!")
            return HttpResponse("Product kommentariyasi muvaffaqiyatli yaratildi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = ProductCommentForm()
    context = {
        'form': form,
    }
    return render(request, 'product/foradmin/color_create.html', context)


def product_comment_update(request, id):
    comment = get_object_or_404(ProductComment, pk=id)
    if request.method == "POST":
        form = ProductCommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product kommentariyasi muvaffaqiyatli yangilandi")
            return HttpResponse("Product kommentariyasi muvaffaqiyatli yangilandi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = ProductCommentForm(instance=comment)
    context = {
        'form': form,
    }
    return render(request, 'product/foradmin/color_update.html', context)


def procuct_comment_delete(request, slug):
    comment = get_object_or_404(ProductComment, id=id)
    comment.delete()
    return redirect('color_list')
# end ProductComment

# We should remake it
# ProductDiscount
def prod_discount_create(request, slug, id=None):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        form = ProductCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            if id:
                prod_comment = get_object_or_404(ProductComment, pk=id)
                comment.parent = prod_comment
            comment.save()
            messages.success(request, "Product kommentariyasi muvaffaqiyatli yaratildi!")
            return HttpResponse("Product kommentariyasi muvaffaqiyatli yaratildi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = ProductCommentForm()
    context = {
        'form': form,
    }
    return render(request, 'product/foradmin/color_create.html', context)


def procuct_comment_update(request, id):
    comment = get_object_or_404(ProductComment, pk=id)
    if request.method == "POST":
        form = ProductCommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product kommentariyasi muvaffaqiyatli yangilandi")
            return HttpResponse("Product kommentariyasi muvaffaqiyatli yangilandi!")
        else:
            messages.error(request, "Forma to'ldirilishida xatolik mavjud!")
    else:
        form = ProductCommentForm(instance=comment)
    context = {
        'form': form,
    }
    return render(request, 'product/foradmin/color_update.html', context)


def product_comment_delete(request, slug):
    comment = get_object_or_404(ProductComment, id=id)
    comment.delete()
    return redirect('color_list')
# end ProductComment

# for client
def product_item_detail_client(request, slug):
    form = CartAddProductForm()
    product_item = ProductItem.objects.select_related('product').prefetch_related('images').get(is_deleted=False, is_archive=False, slug=slug)

    return render(request, 'products/for_client/product_details.html', {'product_item': product_item, 'form': form})


def shop_category(request, slug):
    currency_price = Currency.objects.get(code=get_currency_from_session(request)).price

    f_brands = Q()
    ordering = '-order_count'

    category = get_object_or_404(Category, slug=slug, active=True)
    
    category_childs = Category.objects.values('title', 'slug', 'image').filter(
        childs__parent=category, active=True).annotate(prod_count=Count('products'))

    product_items = ProductItem.objects.filter(f_brands, Q(product__category=category) | 
        Q(product__category__parent=category) | Q(product__category__parent__parent=category), 
        is_deleted=False, is_active=True, is_archive=False, 
        count_in_stock__gt=0).annotate(
            price_currency=get_price_like_float('price') / currency_price,
            price_discount=Func(DiscountItem.objects.filter(product_item=OuterRef('pk'), 
                quantity__gt=F('sold_quantity'), is_active=True).values('price')[:1], function='CAST', 
                template = '%(function)s(%(expressions)s AS FLOAT)') / currency_price,
            image=ProductImage.objects.filter(product_item=OuterRef('pk')).values('image_middle')[:1], 
            discount=Sum('discount_item__quantity'), order_count=Sum('order_items__quantity'),
            rating=Avg('ratings__rating')).select_related('product').order_by(ordering)
            
    latest_products = ProductItem.objects.filter(f_brands, (Q(product__category=category) | 
        Q(product__category__parent=category) | Q(product__category__parent__parent=category)), 
        is_deleted=False, is_active=True, is_archive=False, 
        count_in_stock__gt=0).annotate(
            price_currency=get_price_like_float('price') / currency_price,
            price_discount=Func(DiscountItem.objects.filter(product_item=OuterRef('pk'), 
                quantity__gt=F('sold_quantity'), is_active=True).values('price')[:1], function='CAST', 
                template = '%(function)s(%(expressions)s AS FLOAT)') / currency_price,
            image=ProductImage.objects.filter(product_item=OuterRef('pk')).values('image_middle')[:1], 
            discount=Sum('discount_item__quantity'), order_count=Sum('order_items__quantity'),
            rating=Avg('ratings__rating')).select_related('product').order_by('-created')[:5]


    brands = Brand.objects.filter(Q(products__category=category) | Q(products__category__parent=category) | 
        Q(products__category__parent__parent=category)).values('name', 'slug').distinct()[:15]

    paginator = Paginator(product_items, 20)
    page = request.GET.get('page')
    try:
        product_items = paginator.page(page)
    except PageNotAnInteger:
        product_items = paginator.page(1)
    except EmptyPage:
        product_items = paginator.page(paginator.num_pages)
    
    context = {
        'category': category,
        'category_childs': category_childs,
        'product_items': product_items,
        'brands': brands,
        'latest_products': latest_products
    }
    return render(request, 'products/for_client/shop-category.html', context)

@ajax_required
def shop_ajax_category(request, slug):
    category = get_object_or_404(Category, slug=slug, active=True)

    currency_price = Currency.objects.get(code=get_currency_from_session(request)).price

    filter_data = request.session.get('filter')
    sort_data = request.session.get('sort_order')
    
    if not filter_data:
        filter_data = request.session['filter'] = {}
    if not sort_data:
        sort_data = request.session['sort_order'] = {}

    filter_brands = request.GET.getlist('brand')

    if filter_brands and 'all' not in filter_brands:
        f_brands = Q(product__brand__slug__in=filter_brands)
        request.session['filter'] = filter_brands
        request.session.modified = True
        
    elif 'all' in filter_brands:
        request.session['filter'] = {}
        f_brands = Q()
    else:
        if filter_data:
            f_brands = Q(product__brand__slug__in=filter_data)
        else:
            f_brands = Q()

    s_order = request.GET.get('sort')
    if s_order in s_order_list: 
        ordering = s_order
        request.session['sort_order'] = ordering
        request.session.modified = True
    else:
        if sort_data:
            ordering = sort_data
        else:
            ordering = '-order_count'

    product_items = ProductItem.objects.filter(f_brands, (Q(product__category=category) | 
        Q(product__category__parent=category) | Q(product__category__parent__parent=category)),
        is_deleted=False, is_active=True, is_archive=False, 
        count_in_stock__gt=0).annotate(
            price_currency=get_price_like_float('price') / currency_price,
            price_discount=Func(DiscountItem.objects.filter(product_item=OuterRef('pk'), 
                quantity__gt=F('sold_quantity'), is_active=True).values('price')[:1], function='CAST', 
                template = '%(function)s(%(expressions)s AS FLOAT)') / currency_price,
            image=ProductImage.objects.filter(product_item=OuterRef('pk')).values('image_middle')[:1], 
            discount=Sum('discount_item__quantity'), order_count=Sum('order_items__quantity'),
            rating=Avg('ratings__rating')).select_related('product').order_by(ordering)

    paginator = Paginator(product_items, 20)
    page = request.GET.get('page')
    try:
        product_items = paginator.page(page)
    except PageNotAnInteger:
        product_items = paginator.page(1)
    except EmptyPage:
        return HttpResponse('')
        
    return render(request, f'products/for_client/shop-category_prodlist2_ajax.html', {'product_items': product_items})


