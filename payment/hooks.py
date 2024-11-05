from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.conf import settings
import time
from .models import Order

@receiver(valid_ipn_received)
def paypalPaymentReceived(sender, **kwargs):
    # Add a 10 second pause for PayPal to send IPN data
    time.sleep(10)

    # Grab paypal information
    paypalObj = sender

    # Get the Invoice
    invoice = str(paypalObj.invoice)

    # Match the PayPal Invoice to the Order invoice 
    order = Order.objects.get(invoice=invoice)
    order.paid = True
    order.save()