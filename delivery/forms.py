from django import forms 

from .models import Delivery



class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ('delivery_type', 'price', 'time_in_hours')