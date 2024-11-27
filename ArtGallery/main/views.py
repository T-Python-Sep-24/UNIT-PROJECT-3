from django.shortcuts import render
from django.http import HttpRequest

# Home View
def homeView(request: HttpRequest):
    
    return render(request, 'main/index.html')