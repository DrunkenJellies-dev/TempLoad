from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Product, Category  # Make sure to import your models

class StaticViewSiteMap(Sitemap):

    def items(self):
        # Return a list of static view names and category slugs
        categories = list(Category.objects.values_list('name', flat=True))  # Use 'slug' or the field you need
        products = list(Product.objects.values_list('id', flat=True))  # Product IDs
        return ['about', 'home', 'login', 'logout', 'register', 'updatePassword', 
                'updateUser', 'updateInfo'] + categories + products

    def location(self, item):
        if isinstance(item, int):  # Assuming item is a Product ID when it's an integer
            return reverse('product', kwargs={'pk': item})
        elif isinstance(item, str):  # Assuming item is a category slug
            return reverse('category', kwargs={'foo': item})
        return reverse(item)
