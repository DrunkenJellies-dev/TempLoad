from django.urls import path, include
from . import views

urlpatterns = [
    path('paymentSuccess',views.paymentSuccess, name='paymentSuccess'),
    path('paymentFailed',views.paymentFailed, name='paymentFailed'),
    path('checkout',views.checkout, name='checkout'),
    path('billingInfo',views.billingInfo, name='billingInfo'),
    path('processOrder',views.processOrder, name='processOrder'),
    path('shippedDashboard',views.shippedDashboard, name='shippedDashboard'),
    path('notShippedDashboard',views.notShippedDashboard, name='notShippedDashboard'),
    path('orders/<int:pk>', views.orders, name='orders'),
    path('paypal', include("paypal.standard.ipn.urls")),
]
