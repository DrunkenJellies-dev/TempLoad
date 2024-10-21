from django.shortcuts import render

def paymentSuccess(request):
    return render(request, "payment/paymentSuccess.html")
