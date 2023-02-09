from django.urls import path

from . import views 

app_name = 'carts'

urlpatterns = [
    path('add/<int:item_id>/<slug:slug>/', views.cart_add, name='cart_add_details'),
    path('add/<int:item_id>/', views.cart_add, name='cart_add'),
    path('remove/<str:item_id>/', views.cart_remove, name='cart_remove'),
    path('', views.cart_detail, name='cart_detail'),

]
