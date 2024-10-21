from django.urls import path, include
from . import views

urlpatterns = [
    path('paymentSuccess',views.paymentSuccess, name='paymentSuccess'),
]
