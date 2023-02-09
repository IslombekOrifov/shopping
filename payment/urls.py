from django.urls import path

from . import views


app_name = 'payment'

urlpatterns = [
    # braintree
    path('visa/process/', views.braintree_process, name='visa_process'),

    # payme
    path('payme/process/', views.payme_cart_create, name='payme_process'),
    path('payme/verify/', views.payme_verify, name='payme_verify'),

    # all 
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
]
