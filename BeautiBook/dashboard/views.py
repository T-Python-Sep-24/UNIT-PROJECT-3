from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from services.models import Product
from providers.models import Artist



# Create your views here.
def dashboard_view(request:HttpRequest):
    product = Product.objects.all()
    artist = Artist.objects.all()
    data_filter = request.POST.get('data') or request.GET.get('data', 'all')
    sort_option = request.GET.get('sort')

    if data_filter == "products":
        artist = None
        if sort_option == 'newest':
            product =  product.order_by('-id')
        elif sort_option == 'oldest':
            product = product.order_by('id')
    elif data_filter == "artists":
        product = None
        if sort_option == 'newest':
            artist = artist.order_by('-id')
        elif sort_option == 'oldest':
            artist = artist.order_by('id')

    return render(request,"dashboard/dashboard.html",{"product":product,"data_filter":data_filter,"sort_option":sort_option,"artist":artist})