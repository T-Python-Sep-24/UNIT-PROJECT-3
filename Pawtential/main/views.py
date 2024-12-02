from django.shortcuts import render
from django.http import HttpRequest
from pets.models import Pet

# Create your views here.

def home_view(request):
    pets = Pet.objects.all().order_by('-created_at')[:3]
    
    return render(request, 'main/home.html', {'pets': pets})