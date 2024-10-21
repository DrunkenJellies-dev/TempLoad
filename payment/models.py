from django.db import models
from django.contrib.auth.models import User
from store.models import Product

# Shipping Address Model
class ShippingAddress(models.Model):
    # Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    shippingFullName = models.CharField(max_length=255)
    shippingEmail = models.CharField(max_length=255)
    shippingAddress1 = models.CharField(max_length=255)
    shippingAddress2 = models.CharField(max_length=255)
    shippingCity = models.CharField(max_length=255)
    shippingCounty = models.CharField(max_length=255, null=True, blank=True)
    shippingPostcode = models.CharField(max_length=255, null=True, blank=True)
    shippingCountry = models.CharField(max_length=255)
    

    #Don't pluralize address
    class Meta:
        verbose_name_plural = "ShippingAddress"

    def __str__(self):
        return f'ShippingAddress - {str(self.id)}'
    
# Order Model
class Order(models.model):
    # Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    fullName = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    shippingAddress = models.TextField(max_length=15000)
    amountPaid= models.DecimalField(max_digits=10, decimal_places=2)
    dateOrdered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order - {str(self.id)}'
    
  
