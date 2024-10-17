from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

def cartSummary(request):
    return render(request, 'cartSummary.html', {})

def cartAdd(request):
    # Get the Cart
    cart = Cart(request)
    # Test for POST
    if request.POST.get('action') == 'post':
        # Get product
        productId = int(request.POST.get('productId'))
        # Look up the product in the data base
        product = get_object_or_404(Product, id=productId)
        # Save to a session
        cart.add(product=product)

        # Return a response
        response = JsonResponse({'Product Name: ': product.name})
        return response

def cartDelete(request):
    pass

def cartUpdate(request):
    pass