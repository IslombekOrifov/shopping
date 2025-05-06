from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

from .services import upload_avatar_path, get_default_currency
from general.models import Currency


class CustomUser(AbstractUser):
    CHOICE_CURRENCY = (
        ('uzs', 'UZS'),
        ('USD', 'USD'),
        ('RUB', 'RUB'),
        ('EUR', 'EUR'),
    )

    CHOICE_ROLE = (
        ('c', 'Client'),
        ('cd', 'CompanyDirector'),
        ('cm', 'CompanyManager'),
        ('cp', 'CompanyPoster'),
        ('a', 'admin'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, db_index=True)
    terms = models.BooleanField(default=True, db_index=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True) #default=get_default_currency,
    role = models.CharField(max_length=2, choices=CHOICE_ROLE, default=CHOICE_ROLE[0][0], db_index=True)
    company = models.ForeignKey("company.Company", related_name='workers', blank=True, null=True, on_delete=models.SET_NULL)


class UserDataOnDelete(models.Model):
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(db_index=True)
    role = models.CharField(max_length=2, choices=CustomUser.CHOICE_ROLE, default=CustomUser.CHOICE_ROLE[0][0], db_index=True)

    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_avatar_path, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.PositiveSmallIntegerField(blank=True, null=True)

    # card1
    card = models.PositiveSmallIntegerField(blank=True, null=True)
    
    # card1
    card1 = models.PositiveSmallIntegerField(blank=True, null=True)


class Address(models.Model):
    """clean metodda own_address True bo'lganda client yoki client_data ko'rsatilishi shart"""
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    country = models.ForeignKey('Country', related_name='users_adress', null=True, on_delete=models.PROTECT, limit_choices_to={'active': True})
    city = models.ForeignKey('City', related_name='users_adress', null=True, on_delete=models.PROTECT, limit_choices_to={'active': True})
    region = models.ForeignKey('Region', related_name='users_adress', null=True, on_delete=models.PROTECT, limit_choices_to={'active': True})
    addres = models.CharField(max_length=250)
    postal_code = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('client', 'city')

    def __str__(self):
        return f"{self.client if self.client else self.client_data} -> {self.city} address"


    def clean(self, *args, **kwargs):
        if self.client and self.client_data:
            raise ValidationError({'client_data': "kerakmas"}) 


class AbstractAddressBase(models.Model):
    title = models.CharField(max_length=50)
    order = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('order', 'title')
        abstract = True


class Country(AbstractAddressBase):
    def __str__(self):
        return self.title
    

class City(AbstractAddressBase):
    country = models.ForeignKey(Country, related_name='cities', null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f'{self.title} -> {self.country}'


class Region(AbstractAddressBase):
    city = models.ForeignKey(City, related_name='regions', null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f'{self.title} -> {self.city}'