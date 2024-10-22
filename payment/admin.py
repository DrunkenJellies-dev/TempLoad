from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

# Register Model In the Admin System
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# Create order item inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

# Extend Order Model

class OrderAdmin(admin.ModelAdmin):
    model = Order
    inline = [OrderItemInline]

# Unregister order model
admin.site.unregister(Order)

# Re-register our Order and order items
admin.site.register(Order,OrderAdmin)