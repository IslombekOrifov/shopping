from django.urls import path

from . import views


app_name = 'wishlists'

urlpatterns = [
    path('add/<slug:slug>/', views.wishlist_add, name='add'),
    path('remove/<int:id>/', views.wishlist_remove, name='remove'),
    path('', views.wishlist_detail, name='detail'),
]
