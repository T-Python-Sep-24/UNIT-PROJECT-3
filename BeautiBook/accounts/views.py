from django.shortcuts import render ,redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate 
from django.contrib import messages
from .models import Profile

# Create your views here.
def signup_view(request:HttpRequest):
   
    if request.method == "POST":
        try:
            new_user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password"],
                first_name=request.POST["first_name"],
                email=request.POST["email"]
                )
            new_user.save()
            new_profile = Profile(role = new_user,# about_user = request.POST["about_user"],
                                  is_artist = request.POST["is_artist"],
            )
            new_profile.save()
            messages.success(request,"Registered User Successfully","alert-success")
            return redirect("accounts:signin_view")
        except Exception as e:
            print(e)
    
    return render(request,"accounts/signup.html")


def signin_view(request:HttpRequest):

    if request.method == "POST":
        user = authenticate(request,username=request.POST["username"],password=request.POST["password"],)
        if user:
            login(request,user)
            messages.success(request,"logged in successfully","alert-success")
            return redirect("main:home_view")
        else:
            messages.error(request,"please try again","alert-danger")
    return render (request,"accounts/signin.html")

def logout_view(request:HttpRequest):
    logout(request)
    return redirect("main:home_view")

def user_profile_view(request:HttpRequest,user_name):
    user = User.objects.get(username=user_name)
    profile:Profile = user.profile
    return render(request,'accounts/profile.html',{"user":user})