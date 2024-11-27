from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from funds_app.models import Fund
# Create your views here.

def home_view(request: HttpRequest):

    funds = Fund.objects.all()[:3]

    return render(request, 'index.html', context={'funds': funds})