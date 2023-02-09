from django import forms

from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('desc', 'transaction_code', 'fact_deliveried', 'delivery', 'is_success')


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('product_item', 'order', 'quantity', 'price')


class OrderAddressForm(forms.Form):
    senderRegion = forms.CharField(widget=forms.TextInput, required=True)
    senderCity = forms.CharField(widget=forms.TextInput, required=True)
    address = forms.CharField(widget=forms.TextInput, required=True)
    home_number = forms.CharField(widget=forms.TextInput, required=True)
    postal_code = forms.IntegerField(widget=forms.NumberInput, required=True)
    phone = forms.CharField(widget=forms.TextInput, required=True, max_length=18)
    terms = forms.BooleanField(widget=forms.CheckboxInput, required=True)
    order_desc = forms.CharField(widget=forms.TextInput, required=True, max_length=200)
