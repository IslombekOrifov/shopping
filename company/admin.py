from django.contrib import admin
from .models import Company, CompanyAddress

# Register your models here.

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('director', 'name', 'slug', 'image', 'inn', 'created', 'updated', 'is_deleted')
    list_filter = ('created', 'updated')
    ordering = ('director', 'name', 'created', 'updated')
    prepopulated_fields = {'slug': ('name',)}




@admin.register(CompanyAddress)
class CompanyAddressAdmin(admin.ModelAdmin):
    list_display = ('company', 'city', 'district', 'address', 'email', 'tel1', 'main_add')
    ordering = ('id', 'company', 'city')