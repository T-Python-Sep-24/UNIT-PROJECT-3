from django.shortcuts import render
from django.http import HttpRequest

# Create your views here.


def login_view():
    pass

def register_view(request):
    
    return render(request,'accounts/registration.html')