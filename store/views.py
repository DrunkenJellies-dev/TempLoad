from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserForm, UpdatePasswordForm, UserInfoForm
from django.db.models import Q
import json
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress

def search(request):
    # Determine if they have filled out the form
    if request.method == "POST":
        search = request.POST['searched']
        # Query the product DB model (using icontains to ignore cases sensitivity)
        searched = Product.objects.filter(Q(name__icontains=search) | Q(description__icontains=search))

        # Test for Null
        if not searched:
            messages.success(request, ("Sorry the product " + search + " doesn't exist, please ty again."))
            return render(request, 'search.html', {})
        
        else:
            # Return the page with the searched variable
            return render(request, 'search.html', {'searched':searched})

    else:
        # Return the page
        return render(request, 'search.html', {})


def updateInfo(request):
    if request.user.is_authenticated:
        # Get current user
        currentUser = Profile.objects.get(id=request.user.id)
        # Get current user shipping info
        shippingUser = ShippingAddress.objects.get(id=request.user.id)

        # Get original user form
        form = UserInfoForm(request.POST or None, instance=currentUser)

        # Get user shipping form
        shippingForm = ShippingForm(request.POST or None, instance=shippingUser)

        # Check if the form is valid
        if form.is_valid() or shippingForm.is_valid():
            # Save original form
            form.save()
            # Save shipping form 
            shippingForm.save()

            #Send message 
            messages.success(request, (currentUser.email + " has been updated."))

            #redirect to home
            return redirect('home')
        
        # Return the updateInfo.html page 
        return render(request, 'updateInfo.html', {'form':form, 'shippingForm':shippingForm})
    else:
        messages.success(request, ("You must be logged in to access that page."))
        return redirect('home')

def updatePassword(request):
    if request.user.is_authenticated:
        currentUser = User.objects.get(id=request.user.id)
        # Is the form filled out 
        if request.method == 'POST':
            form = UpdatePasswordForm(currentUser, request.POST)
            # Is the form Valid
            if form.is_valid():
                form.save()
                messages.success(request, ("Your password has been updated. Please login again."))
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('updatePassword')
        else:
            form = UpdatePasswordForm(currentUser)
            return render(request, 'updatePassword.html', {'form':form})
    else:
        messages.success(request, ("You must be logged in to view the page."))
        return redirect('home')

def updateUser(request):
    if request.user.is_authenticated:
        currentUser = User.objects.get(id=request.user.id)
        userForm = UpdateUserForm(request.POST or None, instance=currentUser)

        if userForm.is_valid():
            userForm.save()

            login(request, currentUser)
            messages.success(request, (currentUser.email + " has been updated."))
            return redirect('home')
        return render(request, 'updateUser.html', {'userForm':userForm})
    else:
        messages.success(request, ("You must be logged in to access that page."))
        return redirect('home')

def categorySummary(request):
    categories = Category.objects.all()
    return render(request, 'categorySummary.html', {"categories":categories})

def category(request, foo):
    # Replace Hyphens With Spaces
    foo = foo.replace('-', ' ')
    # Get The Category From The URL
    try:
        # Look Up The Category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, ("That category doesn't exist."))
        return redirect('home')

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def loginUser(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Get the current user
            currentUser = Profile.objects.get(user__id=request.user.id)

            # Get their saved cart from the profile
            savedCart = currentUser.oldCart

            # Check if there is anything in the oldCart
            if savedCart:
                # Convert string to a dictionary
                convertedCart = json.loads(savedCart)

                # Get the Cart
                cart = Cart(request)

                # Loop through the cart and add the items from the database
                for key, value in convertedCart.items():
                    cart.dbAdd(product=key, quantity=value)

            messages.success(request, ("You've been logged in."))
            return redirect('home')
        else:
            messages.success(request, ("There was an error, please try again."))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logoutUser(request):
    logout(request)
    messages.success(request, ("You've been logged out."))
    return redirect('home')

def registerUser(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Login User
            user=authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have registered successfully and are now logged in."))
            return redirect('updateInfo')
        else:
            messages.success(request, ("There was a problem registering your account. Please try again."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})