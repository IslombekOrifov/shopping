from django import forms

from .models import Discount, DiscountItem

class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ('title', 'discount_type', 'image', 'discount_price_or_percent', 'start_date', 'end_date')


class DiscountItemForm(forms.ModelForm):
    class Meta:
        model = DiscountItem
        fields = ('quantity', 'desc', 'product_item', 'category',)