from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from uuid import uuid4

from accounts.models import CustomUser, UserDataOnDelete
from products.models import ProductItem
from company.models import Company
from discounts.models import Discount, DiscountItem


class Order(models.Model):
    CHOICE_STATUS = (
        ('np', 'Not paid'),
        ('do', 'At the departure office'),
        ('ca', 'Courier accepted'),
        ('it', 'In transit'),
        ('dd', 'Delivered'),
        ('sr', 'Sender rejection'),
        ('rn', 'Return'),
        ('wc', 'Waiting for confirmation'),
        ('nc', 'Not confirmed'),

    )
    slug = models.SlugField(max_length=150, blank=True) # blankni ob tasha, unique qo'shib qo'y
    desc = models.CharField(max_length=200, blank=True)
    transaction_code = models.CharField(max_length=150, blank=True)
    
    fact_deliveried = models.DateField(blank=True, null=True)
    
    client = models.ForeignKey(CustomUser, related_name='orders', on_delete=models.SET_NULL, null= True)
    client_data = models.ForeignKey(UserDataOnDelete, blank=True, null=True, on_delete=models.PROTECT)
    delivery = models.CharField(max_length=150, blank=True)

    status = models.CharField(max_length=3, choices=CHOICE_STATUS, default=CHOICE_STATUS[0][0])

    payment_type = models.CharField(max_length=4, blank=True)
    total_price = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True) # blanklarni ob tasha
    currency_course = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    total_price_in_usd = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True) # blanklarni ob tasha
    
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=14)
    terms = models.BooleanField(default=False)
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    
    is_paid = models.BooleanField(default=False)
    is_success = models.BooleanField(default=False)

    product_company = models.ForeignKey(Company, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(uuid4())
        super().save(*args, **kwargs)

    def clean(self):
        if self.client and self.client_data:
            raise ValidationError({'client_data': "Kerakmas!"})

    def __str__(self) -> str:
        return f'Order {self.id}'

    # def get_total_cost(self):
    #     return sum(item.get_cost() for item in self.items.all())

    
class OrderItem(models.Model):
    product_item = models.ForeignKey(ProductItem, related_name='order_items', on_delete=models.PROTECT)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=13, decimal_places=2)
    price_in_usd = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True) # blanklarni ob tashla
    currency_course = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    discount_price = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
    discount_id = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity        