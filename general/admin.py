from django.contrib import admin

from .models import Currency, Faqs   


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'symbol', 'price', 'updated', 'is_active', 'author', 'who_updated')


@admin.register(Faqs)
class FaqsAdmin(admin.ModelAdmin):
    list_display = ('question', 'updated', 'is_active', 'author', 'author_data', 'who_updated', 'author', 'who_updated')