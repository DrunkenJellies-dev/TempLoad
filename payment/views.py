from django.shortcuts import redirect, render
from cart.cart import Cart
from payment.forms import PaymentForm, ShippingForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Product, Profile
import datetime

# Import PayPal libraries
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the order
        orders = Order.objects.get(id=pk)
        # Get the order Items
        items = OrderItem.objects.filter(order.pk)

        if request.POST:
            status = request.POST['shippingStatus']
            # Check if true of false
            if status == "true":
                # Get the Order
                order = Order.objects.filter(id=pk)
                # Get the current date time
                now = datetime.datetime.now()
                # Update the status
                order.update(shipped=True, dateShipped=now)
            else:
                # Get the Order
                order = Order.objects.filter(id=pk)
                # Get the current date time
                now = datetime.datetime.now()
                # Update the status
                order.update(shipped=False, dateShipped=now)
            messages.success(request, "Shipping Status Updated.")
            return redirect('home')
                


        return render(request, "payment/orders.html", {"orders":orders, "items":items})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def shippedDashboard(request):
    # Check if user is superuser
    if request.user.is_authenticated and request.user.is_superuser:
        # Get orders
        orders = Order.objects.filter(shipped=False)

        if request.POST:
            # Get the Status
            status = request.POST['shippingStatus']

            # Get the num
            num = request.POST['num']

            # Get the Order
            order = Order.objects.filter(id=num)

            # Get the current date time
            now = datetime.datetime.now()

            # Update the status
            order.update(shipped=True, dateShipped=None)
            
            messages.success(request, "Shipping Status Updated.")
            return redirect('home')

        return render(request, "payment/shippedDashboard.html", {"orders":orders})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')

def notShippedDashboard(request):
    # Check if user is superuser
    if request.user.is_authenticated and request.user.is_superuser:
        # Get orders
        orders = Order.objects.filter(shipped=False)

        if request.POST:
            # Get the Status
            status = request.POST['shippingStatus']

            # Get the num
            num = request.POST['num']

            # Get the Order
            order = Order.objects.filter(id=num)

            # Get the current date time
            now = datetime.datetime.now()
            
            # Update the status
            order.update(shipped=False, dateShipped=now)
            
            messages.success(request, "Shipping Status Updated.")
            return redirect('home')

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

            # Delete Cart from database (oldCartField)
            currentUser = Profile.objects.filter(user__id=request.user.id)
            # Delete shipping cart in database 
            currentUser.update(oldCart="")
                        

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

      # Get order Information
      fullName = myShipping['shippingFullName']
      email = myShipping['shippingEmail']

      # Create Shipping Address from session info
      shippingAddress = f"{myShipping['shippingAddress1']}\n{myShipping['shippingAddress2']}\n{myShipping['shippingCity']}\n{myShipping['shippingCounty']}\n{myShipping['shippingPostcode']}\n{myShipping['shippingCountry']}\n"

      amountPaid = total

      # Get Host
      host = request.get_host()

      # Create Invoice
      invoice = str(uuid.uuid4())

      # Create PayPal Form Directory
      paypalDict = {
          'business': settings.PAYPAL_RECEIVER_EMAIL,
          'amount': total,
          'item_name':'TempLoad Order',
          'no_shipping': '2',
          'invoice': invoice,
          'currency_code': 'GBP',
          'notify_url': 'https://{}{}'.format(host, reverse("paypal-ipn")),
          'return_url': 'https://{}{}'.format(host, reverse("paymentSuccess")),
          'cancel_return': 'https://{}{}'.format(host, reverse("paymentFailed"))
      }

      # Create PayPal Form
      paypalForm = PayPalPaymentsForm(initial=paypalDict)

      # Check to if the user is logged in
      if request.user.is_authenticated:
          # Get the billing form
          billingForm = PaymentForm()

          # User is logged in
          user = request.user
          
          # Create order
          createOrder = Order(user=user, fullName=fullName, email=email, shippingAddress=shippingAddress, amountPaid=amountPaid, invoice=invoice)
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

          # Delete Cart from database (oldCartField)
          currentUser = Profile.objects.filter(user__id=request.user.id)
          # Delete shipping cart in database 
          currentUser.update(oldCart="")
                        

          return render(request, "payment/billingInfo.html", {"paypalForm": paypalForm, "cartProducts":cartProducts, "quantities":quantities, "total":total, "shippingInfo":request.POST, "billingForm":billingForm })
      else:
          # User is not logged in 
          #Create order
          createOrder = Order(fullName=fullName, email=email, shippingAddress=shippingAddress, amountPaid=amountPaid, invoice=invoice)
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

          # Not logged in
          # Get the billing form
          billingForm = PaymentForm()
          return render(request, "payment/billingInfo.html", {"paypalForm": paypalForm, "cartProducts":cartProducts, "quantities":quantities, "total":total, "shippingInfo":request.POST, "billingForm":billingForm })
      
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
    # Delete the browser cart
    # Get the cart
    cart = Cart(request)
    # Get the products from the cart
    cartProducts = cart.getProducts
    quantities = cart.getQuantities
    total = cart.cartTotal()

    # Delete our cart
    for key in list(request.session.keys()):
        if key == "sessionKey":
            # Delete the key
            del request.session[key]
    return render(request, "payment/paymentSuccess.html")

def paymentFailed(request):
    return render(request, "payment/paymentFailed.html")
