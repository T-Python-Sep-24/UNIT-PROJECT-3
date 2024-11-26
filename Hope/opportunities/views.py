from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse

# Create your views here.

def all_opportunities_view(request:HttpRequest):
    
    return render(request, 'opportunities/all_opportunities.html')
