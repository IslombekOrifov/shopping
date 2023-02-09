from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Avg, Sum, Q, Subquery, OuterRef, F, DecimalField, ExpressionWrapper, Value, Func, FloatField
from django.db.models.functions import JSONObject, Cast
from django.http import Http404, HttpResponse
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from decimal import Decimal, ROUND_UP

from common.decorators import ajax_required, is_ajax
from common.db_classes import Round2
from common.services import get_price_like_float

from .services import get_currency_from_session
from .models import Currency, Faqs, Contact, AboutUs, AboutUsGroup, AboutUsPlus, AboutUsThing

from accounts.models import CustomUser
from accounts.services import get_currency
from products.models import Product, Category, ProductItem, ProductImage, Brand
from products.services import s_order_list
from discounts.models import Discount, DiscountItem


def currency_change(request, code):
    request.session[settings.CURRENCY_SESSION_ID] = code
    request.session.modified = True
    return redirect(request.META['HTTP_REFERER'])


@ajax_required
def index_top_section(request, top_section):
    currency_price = Currency.objects.get(code=get_currency_from_session(request)).price
    if top_section in ('sale', 'stars', 'created'):
        order_field = top_section
    else:
        order_field = 'created'

    top_section_prod = ProductItem.objects.filter(is_deleted=False, is_archive=False, is_active=True).annotate(
        price_currency=get_price_like_float('price') / currency_price,
        price_discount=Func(DiscountItem.objects.filter(product_item=OuterRef('pk'), 
            quantity__gt=F('sold_quantity'), is_active=True).values('price')[:1], function='CAST', 
            template = '%(function)s(%(expressions)s AS FLOAT)') / currency_price,
        image=ProductImage.objects.filter(product_item=OuterRef('pk') ).values('image_middle')[:1], 
        sale=Sum('discount_item__quantity'), stars=Avg('ratings__rating')).order_by(f'-{order_field}')[:8].select_related('product')

    return render(request, 'general/featureds_tab.html', {'top_section_prod': top_section_prod})


@ajax_required
def index_deals_section(request, deals_section):
    currency_price = Currency.objects.get(code=get_currency_from_session(request)).price
    deals_category = get_object_or_404(Category, slug=deals_section)
    product_items = ProductItem.objects.filter(is_deleted=False, is_active=True, is_archive=False, 
        product__category=deals_category, count_in_stock__gt=0).annotate(
            price_currency=get_price_like_float('price') / currency_price,
            price_discount=Func(DiscountItem.objects.filter(product_item=OuterRef('pk'), 
                quantity__gt=F('sold_quantity'), is_active=True).values('price')[:1], function='CAST', 
                template = '%(function)s(%(expressions)s AS FLOAT)') / currency_price,
            image=ProductImage.objects.filter(product_item=OuterRef('pk')).values('image_middle')[:1], 
                discount=Sum('discount_item__quantity')).order_by('-discount', '-discount_item__discount__updated', 
                    '-views_count')[:9].select_related('product')
    return render(request, 'general/best_deals_section.html', {'product_items': product_items})


def index(request):
    currency_price = Currency.objects.get(code=get_currency_from_session(request)).price
    top_section_prod = ProductItem.objects.filter(is_deleted=False, is_archive=False, is_active=True).annotate(
        price_currency=get_price_like_float('price') / currency_price,
        price_discount=Func(DiscountItem.objects.filter(product_item=OuterRef('pk'), 
            quantity__gt=F('sold_quantity'), is_active=True).values('price')[:1], function='CAST', 
            template = '%(function)s(%(expressions)s AS FLOAT)') / currency_price,
        image=ProductImage.objects.filter(product_item=OuterRef('pk')
            ).values('image_middle')[:1], sale=Sum('discount_item__quantity'), stars=Avg('ratings__rating')
                ).order_by('-created')[:8].select_related('product')

    product_items = ProductItem.objects.filter(is_deleted=False, is_active=True, is_archive=False, 
        count_in_stock__gt=0).annotate(price_currency=get_price_like_float('price') / currency_price,
        price_discount=Func(DiscountItem.objects.filter(product_item=OuterRef('pk'), 
            quantity__gt=F('sold_quantity'), is_active=True).values('price')[:1], function='CAST', 
            template = '%(function)s(%(expressions)s AS FLOAT)') / currency_price, 
        image=ProductImage.objects.filter(product_item=OuterRef('pk')).values('image_middle')[:1], 
        discount=Sum('discount_item__quantity')
                ).order_by('-discount', '-discount_item__discount__updated', '-views_count')[:9].select_related('product')

    cat_with_products = Category.objects.filter(active=True, childs__isnull=True).annotate(
        prods_order_count=Sum('products__items__order_items__quantity'),
        prods_view_count=Sum('products__items__views_count'),
        prods_discount_count=Sum('products__items__discount_item__quantity')
    ).order_by('-prods_discount_count', '-prods_order_count', '-prods_view_count')[:7]
    
    best_sellers = ProductItem.objects.filter(is_deleted=False, is_archive=False).annotate(
        price_currency=get_price_like_float('price') / currency_price,
        price_discount=Func(DiscountItem.objects.filter(product_item=OuterRef('pk'), 
            quantity__gt=F('sold_quantity'), is_active=True).values('price')[:1], function='CAST', 
            template = '%(function)s(%(expressions)s AS FLOAT)') / currency_price,
        image=ProductImage.objects.filter(product_item=OuterRef('pk')).values('image_middle')[:1], 
            order_count=Sum('order_items__quantity')).order_by('-order_count')[:24].select_related('product')

    context = {
        'top_section_prod': top_section_prod,
        'cat_with_products': cat_with_products,
        'product_items': product_items,
        'best_sellers': best_sellers,
    }
    return render(request, 'general/index.html', context)


def category_show_detail(request, slug):   
    currency_price = Currency.objects.get(code=get_currency_from_session(request)).price

    category = get_object_or_404(Category, slug=slug, active=True)
    category_childs = Category.objects.values('title', 'slug', 'image').filter(
        parent=category, active=True).annotate(prod_count=Count('products'))

    latest_products = ProductItem.objects.filter((Q(product__category=category) | Q(product__category__parent=category) | 
        Q(product__category__parent__parent=category)), is_deleted=False, is_active=True, is_archive=False, 
        count_in_stock__gt=0).annotate(price_currency=get_price_like_float('price') / currency_price,
            price_discount=Func(DiscountItem.objects.filter(product_item=OuterRef('pk'), 
                quantity__gt=F('sold_quantity'), is_active=True).values('price')[:1], function='CAST', 
                template = '%(function)s(%(expressions)s AS FLOAT)') / currency_price,
            image=ProductImage.objects.filter(product_item=OuterRef('pk')).values('image_middle')[:1], 
            discount=Sum('discount_item__quantity'), order_count=Sum('order_items__quantity'),
            rating=Avg('ratings__rating')).select_related('product').order_by('-created')[:5]

    best_sellers = ProductItem.objects.filter((Q(product__category=category) | Q(product__category__parent=category) | 
        Q(product__category__parent__parent=category)), is_deleted=False, is_active=True, is_archive=False, 
        count_in_stock__gt=0).annotate(price_currency=get_price_like_float('price') / currency_price,
            price_discount=Func(DiscountItem.objects.filter(product_item=OuterRef('pk'), 
                quantity__gt=F('sold_quantity'), is_active=True).values('price')[:1], function='CAST', 
                template = '%(function)s(%(expressions)s AS FLOAT)') / currency_price,
            image=ProductImage.objects.filter(product_item=OuterRef('pk')).values('image_middle')[:1], 
            order_count=Sum('order_items__quantity')).select_related('product').order_by('-order_count')[:9]

    top_rated = ProductItem.objects.filter((Q(product__category=category) | Q(product__category__parent=category) | 
        Q(product__category__parent__parent=category)), is_deleted=False, is_active=True, is_archive=False, 
        count_in_stock__gt=0).annotate(price_currency=get_price_like_float('price') / currency_price,
            price_discount=Func(DiscountItem.objects.filter(product_item=OuterRef('pk'), 
                quantity__gt=F('sold_quantity'), is_active=True).values('price')[:1], function='CAST', 
                template = '%(function)s(%(expressions)s AS FLOAT)') / currency_price,
            image=ProductImage.objects.filter(product_item=OuterRef('pk')).values('image_middle')[:1], 
            rating=Avg('ratings__rating')).select_related('product').order_by('-rating')[:9]

    
    brands_in_category = Brand.objects.filter((Q(products__category=category) | Q(products__category__parent=category) | 
        Q(products__category__parent__parent=category)), active=True).distinct()
    

    context = {
        'category': category,
        'category_childs': category_childs,
        'latest_products': latest_products,
        'best_sellers': best_sellers,
        'top_rated': top_rated,
        'brands_in_category': brands_in_category
    }
    return render(request, 'general/product-categories.html', context)


def faqs_detail(request):
    faqs = Faqs.objects.filter(is_active=True)
    return render(request, 'general/faqs.html', {'faqs': faqs})


def contact_detail(request):
    contact_page = Contact.objects.filter(is_active=True)[:1]
    return render(request, 'general/contact.html', {'contact_page': contact_page})


def about_detail(request):
    about = AboutUs.objects.filter(is_active=True)[:1].prefetch_related('things').prefetch_related('groups').prefetch_related('pluss')
    return render(request, 'general/aboutus.html', {'about': about})


def search(request):
    currency_price = Currency.objects.get(code=get_currency_from_session(request)).price

    search_title = request.GET.get('search')

    sort_data = request.session.get('sort_order')
    
    if not sort_data:
        sort_data = request.session['sort_order'] = {}


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

    product_items = ProductItem.objects.filter((Q(title__icontains=search_title) | Q(product__brand__name__icontains=search_title)),
        is_deleted=False, is_active=True, is_archive=False, 
        count_in_stock__gt=0).annotate(
            price_currency=get_price_like_float('price') / currency_price,
            price_discount=Func(DiscountItem.objects.filter(product_item=OuterRef('pk'), 
                quantity__gt=F('sold_quantity'), is_active=True).values('price')[:1], function='CAST', 
                template = '%(function)s(%(expressions)s AS FLOAT)') / currency_price,
            image=ProductImage.objects.filter(product_item=OuterRef('pk')).values('image_middle')[:1], 
            discount=Sum('discount_item__quantity'), order_count=Sum('order_items__quantity'),
            rating=Avg('ratings__rating')
        ).select_related('product').order_by(ordering)

    latest_products = ProductItem.objects.filter(
        is_deleted=False, is_active=True, is_archive=False, 
        count_in_stock__gt=0).annotate(
            price_currency=get_price_like_float('price') / currency_price,
            price_discount=Func(DiscountItem.objects.filter(product_item=OuterRef('pk'), 
                quantity__gt=F('sold_quantity'), is_active=True).values('price')[:1], function='CAST', 
                template = '%(function)s(%(expressions)s AS FLOAT)') / currency_price,
            image=ProductImage.objects.filter(product_item=OuterRef('pk')).values('image_middle')[:1], 
            discount=Sum('discount_item__quantity'), order_count=Sum('order_items__quantity'),
            rating=Avg('ratings__rating')
            ).select_related('product').order_by('-created')[:8]

    paginator = Paginator(product_items, 20)
    page = request.GET.get('page')
    try:
        product_items = paginator.page(page)
    except PageNotAnInteger:
        product_items = paginator.page(1)
    except EmptyPage:
        if is_ajax(request):
            return HttpResponse('')
        product_items = paginator.page(paginator.num_pages)
        
    if is_ajax(request):
        return render(request, 'general/search-ajax.html', {'product_items': product_items})

    context = {
        'product_items': product_items,
        'latest_products': latest_products
    }
    return render(request, 'general/search.html', context)


    # top_section_prod = Product.objects.filter(is_deleted=False, is_archive=False).annotate(item=ProductItem.objects.filter(
    #         is_active=True, is_deleted=False, count_in_stock__gt=0, product=OuterRef("pk")).annotate(
    #             image=ProductImage.objects.filter(product_item=OuterRef('pk') ).values('image_middle')[:1]).values(
    #                 data=JSONObject(id='id', price='price', image='image'))[:1], sale=Sum('items__discount_item__quantity'),
    #                 rating_star=Avg('ratings__rating')).order_by(f'-{order_field}')[:8]
