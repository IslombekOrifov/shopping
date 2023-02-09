from django.urls import path
from . import views

app_name = 'general'

urlpatterns = [
    path('category/show/<slug:slug>/', views.category_show_detail, name='category_show_detail'),
    path('index/deals/<str:deals_section>/', views.index_deals_section, name='index_deals_section'),
    path('index/top/<str:top_section>/', views.index_top_section, name='index_top_section'),
    path('currency/change/<slug:code>/', views.currency_change, name='currency_change'),
    path('contact/', views.contact_detail, name='contact'),
    path('about/', views.about_detail, name='about'),
    path('search/', views.search, name='search'),
    path('faqs/', views.faqs_detail, name='faqs'),
    path('', views.index, name='index'),
]
