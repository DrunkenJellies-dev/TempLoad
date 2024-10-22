from django.shortcuts import render
from cart.cart import Cart

def checkout(request):
    # Get the cart
    cart = Cart(request)
    # Get the products from the cart
    cartProducts = cart.getProducts
    quantities = cart.getQuantities
    total = cart.cartTotal()
    return render(request, 'payment/checkout.html', {"cartProducts":cartProducts, "quantities":quantities, "total":total})

def paymentSuccess(request):
    return render(request, "payment/paymentSuccess.html")
