from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
# Create your views here.
def signup_view(request:HttpRequest):
    return render(request,"accounts/signup.html")
def signin_view(request:HttpRequest):
    return render(request,"accounts/signin.html")
def logout_view(request:HttpRequest):
    return render(request,"accounts/logout.html")