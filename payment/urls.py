from django.urls import path, include
from . import views

urlpatterns = [
    path('paymentSuccess',views.paymentSuccess, name='paymentSuccess'),
    path('checkout',views.checkout, name='checkout'),
    path('billingInfo',views.billingInfo, name='billingInfo'),
]
