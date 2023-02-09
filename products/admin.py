from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'parent', 'image', 'active', 'who_updated')
    list_filter = ('created', 'updated', 'active')
    ordering = ('title', 'author', 'active', 'who_updated')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'active', 'company', 'who_updated')
    list_filter = ('created', 'updated')
    ordering = ('name', 'author', 'company', 'active', 'created')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'brand', 'author', 'company', 'is_active', 'updated', 'is_deleted', 'is_archive')
    list_filter = ('created', 'updated', 'is_active', 'is_deleted', 'is_archive')
    ordering = ('title', 'category', 'brand', 'author', 'company', 'is_active', 'updated', 'is_deleted', 'is_archive')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'title', 'model', 'price', 'count_in_stock', 'new_count', 'views_count', 'is_active', 'is_deleted')
    list_filter = ('created', 'updated', 'is_active', 'is_deleted')
    ordering = ('product', 'author', 'title', 'model', 'price', 'count_in_stock', 'new_count', 'views_count', 'is_active', 'is_deleted')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product_item', 'image_original')
    ordering = ('product_item',)


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ('product_item', 'user', 'rating', 'created')
    list_filter = ('created',)
    ordering = ('product_item', 'user', 'rating')


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('product_item', 'user', 'parent', 'is_active', 'created', 'updated')
    list_filter = ('created', 'updated', 'is_active')
    ordering = ('product_item', 'user', 'parent', 'is_active', 'created')


