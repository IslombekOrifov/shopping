from django import template
from django.db.models import Sum
from decimal import Decimal, ROUND_UP

from products.models import Brand


register = template.Library()


@register.simple_tag
def get_brands_tag():
    return Brand.objects.values('slug', 'logo').filter(active=True).annotate(
        prods_count=Sum('products__items__order_items__quantity')).order_by('-prods_count')[:20]


@register.filter
def price_change(value):
    output = Decimal(value.quantize(Decimal('.01'), rounding=ROUND_UP))
    return output