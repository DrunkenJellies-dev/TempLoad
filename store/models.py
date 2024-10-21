from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create custom profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=50, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    county = models.CharField(max_length=200, blank=True)
    postcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    oldCart = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
# Create a user profile by default when a user signs in
def createProfile(sender, instance, created, **kwargs):
    if created:
        userProfile = Profile(user=instance)
        userProfile.save()

# Automate the profile creation
post_save.connect(createProfile, sender=User)

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
    
# Customer Model
class Customer(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.firstName} {self.lastName}'
    
# Product Model
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product.')

    # Sales
    isSale = models.BooleanField(default=False)
    salePrice = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def __str__(self) -> str:
        return self.name


# Order Model
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True, null=True)
    phone = models.CharField(max_length=25, default='', blank=True, null=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.product
