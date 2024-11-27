from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def all_funds_view(request: HttpRequest):
    return render(request, 'all_funds.html')


def fund_details_view(request: HttpRequest):
    return None


def add_fund_view(request: HttpRequest):
    return None


def update_fund_view(request: HttpRequest):
    return None