from django.shortcuts import redirect, render
from django.http import HttpRequest,HttpResponse
from .models import Product, Review, Category
from products.forms import ProductForm
from django.contrib import messages

# Create your views here.

def all_product(request:HttpRequest):
    products = Product.objects.all()
    return render(request, 'products/all_product.html', {'products': products})


def detail_product(request:HttpRequest ,product_id:int):
    product = Product.objects.get(pk=product_id)

    return render(request, 'products/detail_product.html', {'product': product})



def add_product(request: HttpRequest):
    categories = Category.objects.all()
    if request.method == "POST": 
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, "Created product successfully", "alert-success")
            return redirect('products:all_product')  
        else:
            print("Not valid form:", product_form.errors)
    else:
        product_form = ProductForm()  

    return render(request, "products/add_product.html",  {'product_form': product_form,'categories': categories })


def update_product(request: HttpRequest, product_id: int):
   
    product = Product.objects.get(pk=product_id)

    categories = Category.objects.all()

    if request.method == "POST": 
       
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, "The product has been updated successfully.", "alert-success")
            return redirect('products:all_product')  
        else:
            
            messages.error(request, "Product update failed. Check data.","alert-danger")
    else:
       
        product_form = ProductForm(instance=product)

   
    return render(request, 'products/update_product.html', {
        'product_form': product_form,
        'categories': categories,
        'product': product,
    })

def delete_product(request: HttpRequest, product_id: int):
    try:
        product = Product.objects.get(pk=product_id)
        product.delete()
        messages.success(request, "The product has been successfully deleted.", "alert-warning")
    except Exception as e:
        print(e)
        
    return redirect('products:all_product') 



