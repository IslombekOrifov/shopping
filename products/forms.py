from django import forms
from django.forms import ClearableFileInput

from .models import *


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title', 'image', 'parent')


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('name', 'logo')

        



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'category', 'brand', 'description', 'is_active', 'is_archive')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].queryset = Category.objects.filter(childs=None)
        self.fields['brand'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_archive'].widget.attrs.update({'class': 'form-check-input'})

    
class ProductItemForm(forms.ModelForm):
    class Meta:
        model = ProductItem
        fields = ('title', 'model', 'price', 'specification', 'count_in_stock', 'is_active')
    
    def __init__(self, *args, **kwargs):
        super(ProductItemForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['model'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['specification'].widget.attrs.update({'class': 'form-control'})
        self.fields['count_in_stock'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})

        
class ProductItemHistoryForm(forms.ModelForm):
    class Meta:
        model = ProductItemHistory
        fields = ('quantity', 'price')


class ProductImageForm(forms.ModelForm):
    image_original = forms.ImageField(widget=ClearableFileInput(attrs={'multiple': True, 'class': 'custom-file-input'}), required=False)

    class Meta:
        model = ProductImage
        fields = ('image_original',)


class ProductRatingForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = ('rating',)


class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ('body',)


