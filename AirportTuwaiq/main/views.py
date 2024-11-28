from django.shortcuts import render,redirect 
from django.http import HttpRequest , HttpResponse
from django.contrib import messages
# Create your views here.

def home_view(request:HttpRequest):

    # messages.info(request, 'This is a global message.')
    if request.user.is_authenticated:
        print( request.user.username)
    else:
        print("........!")
    return render(request, 'main/home.html') 