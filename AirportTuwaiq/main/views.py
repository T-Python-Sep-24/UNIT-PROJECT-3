from django.shortcuts import render,redirect 
from django.http import HttpRequest , HttpResponse
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.


def home_view(request:HttpRequest):
   return render(request, 'main/home.html')

# API Endpoint for Fetching Air Traffic Data (optional)


