from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def sign_up(request:HttpRequest):

    if request.method == "POST":

        try:
            new_user = User.objects.create_user(username=request.POST["username"],password=request.POST["password"],email=request.POST["email"],first_name=request.POST["first_name"],last_name=request.POST["last_name"],)
            new_user.save()
            messages.success(request,"Registered User Successfuly","alert-success")
            return redirect("account:sign_in")
        except Exception as e:
            print(e)

    return render(request,"main/sign_up.html")


def sign_in(request:HttpRequest):
   if request.method == "POST":
       user=authenticate(request,username=request.POST["username"],password=request.POST["password"])
       if user:
           login(request,user)
           messages.success(request,"logged in successfuly","alert-success")
           return redirect("main:home_view")
       else:
           messages.error(request,"try again","alert-warning")

   return render(request,"main/sign_in.html")


def log_out(request:HttpRequest):
    logout(request)
    messages.success(request,"Logout successfully","alert-success")

    return redirect("main:home_view")