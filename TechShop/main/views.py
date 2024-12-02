from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from products.models import Product  

# Create your views here.

def home(request : HttpRequest):
    products = Product.objects.all()
    return render(request, 'main/home.html', {'products': products})
