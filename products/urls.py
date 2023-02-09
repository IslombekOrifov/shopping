from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('detail/seller/<slug:slug>/', views.product_detail_seller, name='product_detail_seller'),
    path('item/create/<slug:slug>/', views.product_item_create, name='product_item_create'),
    path('create/', views.product_create, name='product_create'),
    path('list/', views.product_list_seller, name='product_list_seller'),

    # client
    path('detail/<slug:slug>/', views.product_item_detail_client, name='product_item_detail_client'),
    path('shop/ajax/category/<slug:slug>/', views.shop_ajax_category, name='shop_ajax_category'),
    path('shop/category/<slug:slug>/', views.shop_category, name='shop_category'),
    

]
