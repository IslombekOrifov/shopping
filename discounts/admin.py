from django.contrib import admin

from .models import Discount, DiscountItem


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount_type', 'price_or_percent', 'quantity', 'start_date', 'end_date', 'is_active', 'creator', 'creator_data', 'created')
    # list_filter = ('created', 'updated', 'is_active', 'is_deleted', 'is_archive')
    # ordering = ('title', 'category', 'brand', 'author', 'company', 'is_active', 'updated', 'is_deleted', 'is_archive')
    # prepopulated_fields = {'slug': ('title',)}


@admin.register(DiscountItem)
class DiscountItemAdmin(admin.ModelAdmin):
    list_display = ('product_item', 'discount', 'creator', 'quantity', 'price', 'sold_quantity', 'desc', 'is_active', 'is_deleted')
    # list_filter = ('created', 'updated', 'is_active', 'is_deleted')
    # ordering = ('product', 'author', 'title', 'model', 'price', 'count_in_stock', 'new_count', 'views_count', 'is_active', 'is_deleted')
    # prepopulated_fields = {'slug': ('title',)}
