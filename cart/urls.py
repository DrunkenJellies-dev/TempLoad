from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.cartSummary, name="cartSummary"),
    path('add/', views.cartAdd, name="cartAdd"),
    path('delete/', views.cartDelete, name="cartDelete"),
    path('update/', views.cartUpdate, name="cartUpdate"),
]
