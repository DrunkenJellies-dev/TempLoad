from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('about/',views.about, name='about'),
    path('login/',views.loginUser, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('register/',views.registerUser, name='register'),
    path('product/<int:pk>',views.product, name='product'),
    path('category/<str:foo>',views.category, name='category'),
    path('categorySummary/',views.categorySummary, name='categorySummary'),
]
