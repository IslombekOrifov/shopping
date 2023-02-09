from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # login logout
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # registration
    path('registration/', views.user_register, name='registration'),
    
    # password change
    path('password_change/', views.password_change, name='password_change'),

    # password_reset
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/done', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('details/', views.user_details, name='details'),
    path('orders/', views.user_orders, name='orders'),
    path('wishlist/', views.user_wishlist, name='wishlist'),
    path('carts/', views.user_carts, name='carts'),

    # seller urls
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    
]