from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from django.contrib import messages
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

    return redirect("main:home")



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





@login_required
def add_to_cart(request:HttpRequest, product_id:int):
    product = Product.objects.get(id=product_id)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"Added {product.name} to your cart." , "alert-success")
    
    return redirect('accounts:view_cart')

@login_required
def remove_from_cart(request: HttpRequest, product_id: int):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()
    messages.success(request, f"Removed {product.name} from your cart." , "alert-success")
    return redirect('accounts:view_cart')


@login_required
def view_cart(request: HttpRequest):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)

    if created:
        messages.success(request, "A new cart has been created for you.", "alert-success")

    context = {
        "cart": cart,
        "cart_items": cart_items,
        "total_price": total_price,
        "total_items": total_items,
    }

    return render(request, "accounts/view_cart.html", context)