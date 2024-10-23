from django.shortcuts import redirect, render
from cart.cart import Cart
from payment.forms import PaymentForm, ShippingForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Product

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the order
        orders = Order.objects.get(id=pk)
        # Get the order Items
        items = OrderItem.objects.filter(order.pk)

        return render(request, "payment/orders.html", {"orders":orders, "items":items})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def shippedDashboard(request):
    # Check if user is superuser
    if request.user.is_authenticated and request.user.is_superuser:
        # Get orders
        orders = Order.objects.filter(shipped=False)


        return render(request, "payment/shippedDashboard.html", {"orders":orders})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')

def notShippedDashboard(request):
    # Check if user is superuser
    if request.user.is_authenticated and request.user.is_superuser:
        # Get orders
        orders = Order.objects.filter(shipped=False)

        return render(request, "payment/notShippedDashboard.html", {"orders":orders})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')

def processOrder(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        # Get the products from the cart
        cartProducts = cart.getProducts
        quantities = cart.getQuantities
        total = cart.cartTotal()

        # Get billing information
        paymentForm = PaymentForm(request.POST or None)

        # Get shipping session data
        myShipping = request.session.get('myShipping')

        # Get order Information
        fullName = myShipping['shippingFullName']
        email = myShipping['shippingEmail']

        # Create Shipping Address from session info
        shippingAddress = f"{myShipping['shippingAddress1']}\n{myShipping['shippingAddress2']}\n{myShipping['shippingCity']}\n{myShipping['shippingCounty']}\n{myShipping['shippingPostcode']}\n{myShipping['shippingCountry']}\n"

        amountPaid = total

        # Create an order
        # Check if user is logged in
        if request.user.is_Authenticated:
            # User is logged in
            user = request.user

            # Create order
            createOrder = Order(user=user, fullName=fullName, email=email, shippingAddress=shippingAddress, amountPaid=amountPaid)
            createOrder.save()

            # Add order items
            # Get the Order ID
            orderId = createOrder.pk

            # Get Product Information
            for product in cartProducts:
                # Get product ID
                productId = product.id
                # Get product price
                if product.isSale:
                    price = product.salePrice
                else:
                    price = product.price

                # Get quantity
                for key, value in quantities().items:
                    if int(key) == product.id:
                        # Create order item
                        createOrderItem = OrderItem(order=orderId, product=productId, user=user, quantity=value, price=price)
                        createOrderItem.save()

            # Delete our cart
            for key in list(request.session.keys()):
                if key == "sessionKey":
                    # Delete the key
                    del request.session[key]
                        

            messages.success(request, "Order Placed")
            return redirect('home')
        else:
            # User is not logged in 
            #Create order
            createOrder = Order(fullName=fullName, email=email, shippingAddress=shippingAddress, amountPaid=amountPaid)
            createOrder.save()

            # Add order items
            # Get the Order ID
            orderId = createOrder.pk

            # Get Product Information
            for product in cartProducts:
                # Get product ID
                productId = product.id
                # Get product price
                if product.isSale:
                    price = product.salePrice
                else:
                    price = product.price

                # Get quantity
                for key, value in quantities().items:
                    if int(key) == product.id:
                        # Create order item
                        createOrderItem = OrderItem(order=orderId, product=productId, quantity=value, price=price)
                        createOrderItem.save()

            # Delete our cart
            for key in list(request.session.keys()):
                if key == "sessionKey":
                    # Delete the key
                    del request.session[key]

            messages.success(request, "Order Placed")
            return redirect('home')

    else:
        messages.success(request, "Access Denied")
        return redirect('home')
        

def billingInfo(request):
    if request.POST:
      # Get the cart
      cart = Cart(request)
      # Get the products from the cart
      cartProducts = cart.getProducts
      quantities = cart.getQuantities
      total = cart.cartTotal()

      # Create a session with shipping information
      myShipping = request.POST
      request.session['myShipping'] = myShipping

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
