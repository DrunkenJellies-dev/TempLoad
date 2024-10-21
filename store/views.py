from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserForm, UpdatePasswordForm, UserInfoForm

def search(request):
    # Determine if they have filled out the form
    if request.method == "POST":
        searched = request.POST['searched']
        # Return the page with the searched variable
        return render(request, 'search.html', {'searched':searched})

    else:
        # Return the page
        return render(request, 'search.html', {})


def updateInfo(request):
    if request.user.is_authenticated:
        currentUser = Profile.objects.get(id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=currentUser)

        if form.is_valid():
            form.save()

            messages.success(request, (currentUser.email + " has been updated."))
            return redirect('home')
        return render(request, 'updateInfo.html', {'form':form})
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