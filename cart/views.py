from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cartSummary(request):
    # Get the cart
    cart = Cart(request)
    # Get the products from the cart
    cartProducts = cart.getProducts
    quantities = cart.getQuantities
    total = cart.cartTotal()
    return render(request, 'cartSummary.html', {"cartProducts":cartProducts, "quantities":quantities, "total":total})

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

        # Display a message pop-up
        messages.success(request, (product.name + " has been added to the cart with the quantity of " + str(productQty) + "."))

        # Return a response
        #response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty: ': cartQuantity})
        return response

def cartDelete(request):
     # Get the Cart
    cart = Cart(request)

    # Test for POST
    if request.POST.get('action') == 'post':
        # Get inputs
        productId = int(request.POST.get('productId'))

        # Look up the product in the data base
        product = get_object_or_404(Product, id=productId)

        # Call Delete Function
        cart.delete(product=productId)

        # Display a message pop-up
        messages.success(request, (product.name + " has removed from the cart."))

        # Return a Json Response
        response = JsonResponse({'product':productId})
        return response

def cartUpdate(request):
    # Get the Cart
    cart = Cart(request)

    # Test for POST
    if request.POST.get('action') == 'post':
        # Get inputs
        productId = int(request.POST.get('productId'))
        productQty = int(request.POST.get('productQty'))

        # Look up the product in the data base
        product = get_object_or_404(Product, id=productId)

        # Update the cart
        cart.update(product=productId, quantity=productQty)

        # Display a message pop-up
        messages.success(request, (product.name + " has been updated in the cart with the quantity of " + str(productQty) + "."))

        # Return a Json Response
        response = JsonResponse({'qty':productQty})
        return response