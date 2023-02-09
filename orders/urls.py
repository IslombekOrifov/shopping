from django.urls import path

from . import views

app_name = 'orders'


urlpatterns = [
    path('delete/<slug:slug>/', views.order_delete, name='delete'),
    path('details/<slug:slug>/', views.order_details, name='details'),
    path('', views.order_checkout, name='order_checkout'),
]
