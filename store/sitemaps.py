from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product, Category

class StaticViewSiteMap(Sitemap):
    
    def items(self):
        # Gather categories and products
        categories = Category.objects.values_list('name', flat=True) 
        products = Product.objects.values_list('id', flat=True)
        
        # Combine all items into a single list of URLs
        return [
            'about', 'home', 'login', 'logout', 'register', 
            'updatePassword', 'updateUser', 'updateInfo'
        ] + list(categories) + list(products)

    def location(self, item):
        # Map item type to the appropriate URL
        if isinstance(item, int):  # Product ID
            return reverse('product', kwargs={'pk': item})
        elif isinstance(item, str):  # Category name
            return reverse('category', kwargs={'foo': item})
        return reverse(item)

    def changefreq(self, item):
        # Example: Set different change frequencies based on item type
        if isinstance(item, str) and item in ['home', 'about']:
            return 'monthly'
        return 'weekly'

    def priority(self, item):
        # Example: Set priority based on item type
        if isinstance(item, str) and item in ['home']:
            return 1.0  # High priority for home
        return 0.5  # Default priority
