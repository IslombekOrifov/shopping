from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product_item']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'slug', 'transaction_code', 'status', 'client', 'client_data', 
        'total_price', 'is_paid', 'is_success', 'updated'
    )
    list_filter = ('is_paid', 'is_success', 'terms')
    ordering = ('is_paid', 'is_success', 'terms',  'status', 'client', 'client_data')
    inlines = [OrderItemInline]