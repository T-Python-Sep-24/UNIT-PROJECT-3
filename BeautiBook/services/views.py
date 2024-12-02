from django.shortcuts import render ,redirect , get_object_or_404 
from django.http import HttpRequest,HttpResponse
from .models import Product
from providers.models import Artist
from django.core.paginator import Paginator
# Create your views here.
def products_view(request:HttpRequest):
    products = Product.objects.all()
    paginator = Paginator(products, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "services/products.html", {"products": page_obj})

def add_product_view(request: HttpRequest):
    products = Product.objects.all()  
    if request.method == "POST":
        name = request.POST.get("name")
        about = request.POST.get("about")
        price = request.POST.get("price")
        city = request.POST.get("city")
        image = request.FILES.get("image")
        new_product   = Product(
            name=name,
            about=(about),
            price=float(price),
            city =city,
            image =image,
        )
        new_product.save()
        return redirect("services:products_view")
    return render(request, "services/add_product.html")

def product_detail_view(request:HttpRequest, product_id:int):
    product = Product.objects.get(pk=product_id)
    return render(request,"services/product_detail.html",{"product":product})

def update_product_view(request: HttpRequest,product_id:int):
    product_detail = get_object_or_404(Product,pk=product_id)
    if request.method == "POST":
        product_detail.name = request.POST["name"]
        product_detail.about = request.POST["about"]
        product_detail.city = request.POST["city"]
        product_detail.price = request.POST["price"]
        product_detail.image = request.FILES["image"]
        product_detail.save()
        return redirect("dashboard:dashboard_view")
    return render(request, "services/update_product.html",{"product_detail": product_detail})

def product_delete_view(request:HttpRequest, product_id:int):
    product_detail = Product.objects.get(pk=product_id)
    product_detail.delete()
    return redirect("dashboard:dashboard_view")



