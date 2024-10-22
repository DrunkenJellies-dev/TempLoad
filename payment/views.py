from django.shortcuts import render

def checkout(request):
    return render(request, "payment/checkout.html")

def paymentSuccess(request):
    return render(request, "payment/paymentSuccess.html")
