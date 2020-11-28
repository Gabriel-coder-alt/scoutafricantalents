from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.StoreFront, name='store-front'),
    path('payment_successful/', views.PaymentSuccessful, name='payment_successful'),
    path('payment_not_successful/', views.PaymentNotSuccessful, name='payment_not_successful'),
    path('checkout/<id>/', views.Checkout, name='checkout')
]