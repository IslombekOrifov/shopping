from django import forms
from .models import Company, CompanyAddress


class CompanyForm(forms.ModelForm):
    model = Company
    fields = ('title', 'image', 'inn')


class CompanyAddressForm(forms.ModelForm):
    model = CompanyAddress
    fields = ('city', 'district', 'address', 'email', 'tel1', 'tel2', 'map_url')

