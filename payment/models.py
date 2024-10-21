from django.db import models
from django.contrib.auth.models import User

class ShippingAddress(models.Model):
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