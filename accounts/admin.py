from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets+ (
        (      
            'Custom fields', # you can also use None                 
            {
                'fields': (
                    'currency',
                    'role',
                    'company',
                    'terms'
                ),
            },
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'date_of_birth', 'phone', 'card', 'card1')
    list_filter = ('date_of_birth',)
    ordering = ('user',)

