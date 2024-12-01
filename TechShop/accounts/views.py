from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from django.contrib import messages
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required

from products.models import Product,Review
from .models import Cart, CartItem ,Profile
# Create your views here.



def sign_up(request: HttpRequest):
    if request.method == "POST":

        try:
            with transaction.atomic():
                new_user = User.objects.create_user(username=request.POST["username"],password=request.POST["password"],email=request.POST["email"], first_name=request.POST["first_name"], last_name=request.POST["last_name"])
                new_user.save()

                profile = Profile(user=new_user, about=request.POST["about"])
                profile.save()

            messages.success(request, "Registered User Successfuly", "alert-success")
            return redirect("accounts:sign_in")
        
        except IntegrityError as e:
            messages.error(request, "Please choose another username", "alert-danger")
        except Exception as e:
            messages.error(request, "Couldn't register user. Try again", "alert-danger")
            print(e)
    

    return render(request, "accounts/signup.html")

def sign_in(request: HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!", "alert-success")
            return redirect("main:home")  
        else:
            messages.error(request, "Invalid username or password.", "alert-danger")

    return render(request, "accounts/signin.html")



def log_out(request: HttpRequest):

    logout(request)
    messages.success(request, "logged out successfully", "alert-warning")

    return redirect(request.GET.get("next", "/"))



def user_profile(request:HttpRequest, user_name):
    user = User.objects.get(username=user_name)
    product = Product.objects.first()
    profile = Profile.objects.filter(user=user).first()
    reviews = Review.objects.filter(user=user)


    context = {
        "user": user,
        "profile": profile,
        'product': product,
        'reviews': reviews,
    }

    return render(request, "accounts/user_profile.html", context)




@login_required
def update_user_profile(request: HttpRequest):
    user = request.user
    profile = Profile.objects.filter(user=user).first()

    if request.method == "POST":
       
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.email = request.POST.get("email", user.email)
        user.save()

        if profile:
            profile.about = request.POST.get("about", profile.about)
            profile.save()
        else:
            Profile.objects.create(user=user, about=request.POST.get("about", ""))

        messages.success(request, "Profile updated successfully.", "alert-success")
        return redirect("accounts:update_user_profile")

    context = {
        "user": user,
        "profile": profile,
    }

    return render(request, "accounts/update_profile.html", context)