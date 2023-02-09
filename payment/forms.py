from django import forms


class PaymeCartCreateForm(forms.Form):
    card_number = forms.IntegerField(required=True)
    card_expire = forms.CharField(max_length=4, required=True)


class PaymeCartVerifyForm(forms.Form):
    sms_code = forms.CharField(max_length=15, required=True)
