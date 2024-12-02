from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.
def home_view(request:HttpRequest):

     if request.user.is_authenticated:
          print(request.user.username)
     else:
          print("none")
     return render(request,"main/index.html")