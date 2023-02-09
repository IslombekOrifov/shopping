from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from accounts.models import CustomUser, UserDataOnDelete
from products.models import ProductItem, Category


class Discount(models.Model):
    CHOICE_DISCOUNT_TYPE = (
        ('pe', 'Price'),
        ('pt', 'Protsent')
    )

    creator = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    creator_data = models.ForeignKey(UserDataOnDelete, on_delete=models.CASCADE, blank=True, null=True)
    who_updated = models.ForeignKey(CustomUser, related_name='discount_updated', on_delete=models.SET_NULL, blank=True, null=True)
    
    title = models.CharField(max_length=200)
    image = models.ImageField()
    discount_type = models.CharField(max_length=2, choices=CHOICE_DISCOUNT_TYPE, default=CHOICE_DISCOUNT_TYPE[0][0])
    price_or_percent = models.DecimalField(max_digits=11, decimal_places=2, validators=[MinValueValidator(2.00)])
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(5)])
    
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def clean(self):
        if self.creator and self.creator_data:
            raise ValidationError({'creator_data': 'kerakmas!'})

    def __str__(self) -> str:
        return self.title

class DiscountItem(models.Model):
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT)
    product_item = models.ForeignKey(ProductItem, related_name='discount_item', blank=True, null=True, on_delete=models.PROTECT)
    
    creator = models.ForeignKey(CustomUser, related_name='discount_items', on_delete=models.SET_NULL, null= True)
    creator_data = models.ForeignKey(UserDataOnDelete, on_delete=models.PROTECT, blank=True, null=True)
    who_updated = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(5)])
    price = models.DecimalField(max_digits=11, decimal_places=2)
    sold_quantity = models.PositiveSmallIntegerField()
    booked = models.PositiveSmallIntegerField(blank=True, default=0)
    desc = models.CharField(max_length=300, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    def clean(self):
        if self.creator and self.creator_data:
            raise ValidationError({'creator_data': 'kerakmas!'})

    def __str__(self):
        return f'{self.product_item.title} discount'



