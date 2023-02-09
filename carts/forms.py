from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class':'js-result form-control h-auto border-0 rounded p-0 shadow-none'}), initial=1, required=False, min_value=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)