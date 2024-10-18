from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

def cartSummary(request):
    # Get the cart
    cart = Cart(request)
    # Get the products from the cart
    cartProducts = cart.getProducts
    quantities = cart.getQuantities
    return render(request, 'cartSummary.html', {"cartProducts":cartProducts, "quantities":quantities})

def cartAdd(request):
    # Get the Cart
    cart = Cart(request)
    # Test for POST
    if request.POST.get('action') == 'post':
        # Get inputs
        productId = int(request.POST.get('productId'))
        productQty = int(request.POST.get('productQty'))
        # Look up the product in the data base
        product = get_object_or_404(Product, id=productId)
        # Save to a session
        cart.add(product=product, quantity=productQty)

        # Get cart quantity
        cartQuantity = cart.__len__()

        # Return a response
        #response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty: ': cartQuantity})
        return response

def cartDelete(request):
    pass

def cartUpdate(request):
    # Get the Cart
    cart = Cart(request)

    # Test for POST
    if request.POST.get('action') == 'post':
        # Get inputs
        productId = int(request.POST.get('productId'))
        productQty = int(request.POST.get('productQty'))

        # Update the cart
        cart.update(product=productId, quantity=productQty)

        # Return a Json Response
        response = JsonResponse({'qty':productQty})
        return response