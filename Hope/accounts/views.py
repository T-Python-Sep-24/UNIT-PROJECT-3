from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse

# Create your views here.

def organization_signup_view(request:HttpRequest):
    
    return render(request, 'accounts/organization_signup.html')




def volunteer_signup_view(request:HttpRequest):
    
    return render(request, 'accounts/volunteer_signup.html')




def login_view(request:HttpRequest):
    
    return render(request, 'accounts/login.html')




def logout_view(request:HttpRequest):
    
    return render(request, 'accounts/home.html')
