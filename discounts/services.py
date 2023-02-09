from django.utils import timezone
from django.db.models import F

from .models import DiscountItem


def get_discount_by_product_item(product_item):
    discount = DiscountItem.objects.filter(product_item=product_item, 
        discount__is_active=True, discount__is_deleted=False, discount__end_date__gt=timezone.now(),
        quantity__gt=F('sold_quantity')).annotate(
            can_be_booked=F('quantity') - F('sold_quantity') - F('booked'), booked_filter=F('quantity') - F('sold_quantity')
        ).filter(booked__lt=F('booked_filter'))[:1]
    if discount:
        return discount
    else:
        return None