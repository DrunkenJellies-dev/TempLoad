from django.shortcuts import redirect, render
from cart.cart import Cart
from payment.forms import PaymentForm, ShippingForm
from payment.models import ShippingAddress
from django.contrib import messages

def billingInfo(request):
    if request.POST:
      # Get the cart
      cart = Cart(request)
      # Get the products from the cart
      cartProducts = cart.getProducts
      quantities = cart.getQuantities
      total = cart.cartTotal()

      # Check to if the user is logged in
      if request.user.is_authenticated:
          # Get the billing form
          billingForm = PaymentForm()
          return render(request, "payment/billingInfo.html", {"cartProducts":cartProducts, "quantities":quantities, "total":total, "shippingInfo":request.POST, "billingForm":billingForm })
      else:
          # Not logged in
          # Get the billing form
          billingForm = PaymentForm()
          return render(request, "payment/billingInfo.html", {"cartProducts":cartProducts, "quantities":quantities, "total":total, "shippingInfo":request.POST, "billingForm":billingForm })

          

      
      

    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def checkout(request):
    # Get the cart
    cart = Cart(request)
    # Get the products from the cart
    cartProducts = cart.getProducts
    quantities = cart.getQuantities
    total = cart.cartTotal()

    if request.user.is_authenticated:
          # Checkout as logged in user

          #Shipping User
          shippingUser = ShippingAddress.objects.get(user__id=request.user.id)
          
          #Shipping Form
          shippingForm = ShippingForm(request.POST or None, instance=shippingUser)
          return render(request, "payment/checkout.html", {"cartProducts":cartProducts, "quantities":quantities, "total":total, "shippingForm":shippingForm })
    else:
          shippingForm = ShippingForm(request.POST or None)
          return render(request, "payment/checkout.html", {"cartProducts":cartProducts, "quantities":quantities, "total":total, "shippingForm":shippingForm })

def paymentSuccess(request):
    return render(request, "payment/paymentSuccess.html")
