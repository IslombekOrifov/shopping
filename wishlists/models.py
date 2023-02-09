from django.db import models

from accounts.models import CustomUser
from accounts.validators import is_client
from products.models import Product, ProductItem


class WishedProduct(models.Model):
    client = models.ForeignKey(
        CustomUser, related_name='wishlists', on_delete=models.CASCADE, 
        validators=[is_client]
    )
    product = models.ForeignKey(ProductItem, related_name='wishlists', on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    