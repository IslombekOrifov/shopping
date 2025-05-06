from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django_resized import ResizedImageField
from uuid import uuid4
from colorfield.fields import ColorField
from ckeditor.fields import RichTextField

from accounts.models import CustomUser
from company.models import Company


class CreatedUpdateBase(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class Category(CreatedUpdateBase):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    author = models.ForeignKey(CustomUser, related_name='categories', on_delete=models.SET_NULL, blank=True, null=True)
    author_data = models.ForeignKey(CustomUser, on_delete=models.PROTECT, blank=True, null=True)
    who_updated = models.ForeignKey(CustomUser, related_name='category_updated', on_delete=models.PROTECT, blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey('self', related_name='childs', on_delete=models.PROTECT, blank=True, null=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_child(self):
        sub_cat = Category.objects.filter(parent=self.id)
        return sub_cat

    def get_absolute_url(self):
        return reverse("products:shop_category", kwargs={"slug": self.slug})
    

class Brand(CreatedUpdateBase):
    author = models.ForeignKey(CustomUser, related_name='brands', on_delete=models.SET_NULL, blank=True, null=True)
    author_data = models.ForeignKey(CustomUser, on_delete=models.PROTECT, blank=True, null=True)
    who_updated = models.ForeignKey(CustomUser, related_name='brand_updated', on_delete=models.SET_NULL, blank=True, null=True)
    company = models.ForeignKey(Company, related_name='brands', blank=True, null=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    logo = models.ImageField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class Product(CreatedUpdateBase):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT, limit_choices_to={'active': True})
    author = models.ForeignKey(CustomUser, related_name='products', on_delete=models.SET_NULL, blank=True, null=True)
    author_data = models.ForeignKey(CustomUser, on_delete=models.PROTECT, blank=True, null=True)
    who_updated = models.ForeignKey(CustomUser, related_name='product_updated', on_delete=models.SET_NULL, blank=True, null=True)
    company = models.ForeignKey(Company, related_name='products', on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, related_name='products',on_delete=models.PROTECT, default=1) # default ni obtashla
    description = RichTextField()
    is_archive = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(uuid4())
        super().save(*args, **kwargs)

    
    
class ProductItem(CreatedUpdateBase):
    product = models.ForeignKey(Product, related_name='items', on_delete=models.PROTECT)
    author = models.ForeignKey(CustomUser, related_name='product_items', on_delete=models.SET_NULL, blank=True, null=True)
    author_data = models.ForeignKey(CustomUser, on_delete=models.PROTECT, blank=True, null=True)
    who_updated = models.ForeignKey(CustomUser, related_name='product_item_updated', on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    model = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=13, decimal_places=2)
    count_in_stock = models.PositiveSmallIntegerField(default=0)
    new_count = models.PositiveSmallIntegerField(default=0)
    specification = RichTextField()
    views_count = models.PositiveIntegerField(default=0)
    is_archive = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(uuid4())
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("products:product_item_detail_client", kwargs={"slug": self.slug})


class ProductItemHistory(models.Model):
    author = models.ForeignKey(CustomUser, related_name='product_items_histories', on_delete=models.SET_NULL, blank=True, null=True)
    author_data = models.ForeignKey(CustomUser, on_delete=models.PROTECT, blank=True, null=True)
    product_item = models.ForeignKey(ProductItem, related_name='product_item_histories', on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(max_digits=13, decimal_places=2)
    adder = models.ForeignKey(CustomUser, related_name='product_item_histories', on_delete=models.PROTECT)


class ProductImage(models.Model):
    product_item = models.ForeignKey(ProductItem, related_name='images', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, related_name='product_images', on_delete=models.SET_NULL, blank=True, null=True) # blanklar ---
    author_data = models.ForeignKey(CustomUser, on_delete=models.PROTECT, blank=True, null=True)
    who_updated = models.ForeignKey(CustomUser, related_name='product_image_updated', on_delete=models.SET_NULL, blank=True, null=True)
    image_original = models.ImageField(upload_to='products/')
    image_detail = ResizedImageField(size=[720, 660], crop=['middle', 'center'], quality=100, scale=1, upload_to='products/', blank=True, null=True)
    image_big = ResizedImageField(size=[564, 520], crop=['middle', 'center'], quality=100, scale=1, upload_to='products/', blank=True, null=True)
    image_middle= ResizedImageField(size=[212, 200], crop=['middle', 'center'], quality=100, scale=1, upload_to='products/', blank=True, null=True)
    image_presmall = ResizedImageField(size=[150, 140], crop=['middle', 'center'], quality=100, scale=1, upload_to='products/', blank=True, null=True)
    image_small = ResizedImageField(size=[75, 75], crop=['middle', 'center'], quality=100, scale=1, upload_to='products/', blank=True, null=True)
    image_for_cart = ResizedImageField(size=[300, 300], crop=['middle', 'center'], quality=100, scale=1, upload_to='products/', blank=True, null=True)
    
    class Meta:
        ordering = ('product_item',)
    

class ProductRating(models.Model):
    product_item = models.ForeignKey(ProductItem, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='ratings', blank=True, null=True, on_delete=models.SET_NULL)
    rating = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_item.title} -> {self.rating}"

    
class ProductComment(models.Model):
    product_item = models.ForeignKey(ProductItem, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='comments', blank=True, null=True, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    parent = models.ForeignKey('self', related_name='childs', blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('-updated',)
    
    def __str__(self):
        return f"{self.product_item.title} -> {self.updated}"
    
    
