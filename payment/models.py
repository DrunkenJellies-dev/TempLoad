from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save

# Shipping Address Model
class ShippingAddress(models.Model):
    # Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    shippingFullName = models.CharField(max_length=255)
    shippingEmail = models.CharField(max_length=255)
    shippingAddress1 = models.CharField(max_length=255)
    shippingAddress2 = models.CharField(max_length=255, null=True, blank=True)
    shippingCity = models.CharField(max_length=255)
    shippingCounty = models.CharField(max_length=255, null=True, blank=True)
    shippingPostcode = models.CharField(max_length=255, null=True, blank=True)
    shippingCountry = models.CharField(max_length=255)
    

    #Don't pluralize address
    class Meta:
        verbose_name_plural = "ShippingAddress"

    def __str__(self):
        return f'ShippingAddress - {str(self.id)}'
    
# Create a shipping address by default when a user signs in
def createShipping(sender, instance, created, **kwargs):
    if created:
        userShipping = ShippingAddress(user=instance)
        userShipping.save()

# Automate the shipping creation
post_save.connect(createShipping, sender=User)
    
# Order Model
class Order(models.Model):
    # Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    fullName = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    shippingAddress = models.TextField(max_length=15000)
    amountPaid= models.DecimalField(max_digits=10, decimal_places=2)
    dateOrdered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)

    def __str__(self):
        return f'Order - {str(self.id)}'
    
  
# Order Items Model
class OrderItem(models.Model):
    # Foreign Keys
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f'Order Item - {str(self.id)}'