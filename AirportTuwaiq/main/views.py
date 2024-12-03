from django.shortcuts import render,redirect 
from django.http import HttpRequest , HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from flights .models import Flight

# Create your views here.

def home_view(request:HttpRequest):
    if request.user.is_authenticated:
        print(request.user.username)
    return render(request, 'main/home.html')
    
def riyadh_view(request:HttpRequest):
    return render(request, 'main/riyadh.html')

def jeddah_view(request:HttpRequest):
    return render(request, 'main/jeddah.html')

def abha_view(request:HttpRequest):
    return render(request, 'main/abha.html')


def dammam_view(request:HttpRequest):
    return render(request, 'main/dammam.html')