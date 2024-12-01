from django.shortcuts import redirect, render
from django.http import Http404, HttpRequest,HttpResponse
from .models import Product, Review, Category
from products.forms import ProductForm
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.

def all_product(request:HttpRequest):
    products = Product.objects.all()
    return render(request, 'products/all_product.html', {'products': products})


def detail_product(request, product_id):
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


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Review

def add_review_view(request: HttpRequest, product_id):
    if not request.user.is_authenticated:
        messages.error(request, "Only registered users can add a review.", "alert-danger")
        return redirect("accounts:sign_in")

    if request.method == "POST":
        product_object = get_object_or_404(Product, pk=product_id)

        new_review = Review(
            product=product_object,
            user=request.user,
            comment=request.POST["comment"],
            rating=request.POST["rating"]
        )
        new_review.save()

        messages.success(request, "Review added successfully!", "alert-success")

    return redirect("products:detail_product", product_id=product_id)

def delete_review_view(request: HttpRequest, review_id):
    try:
        review = Review.objects.get(pk=review_id)
        product_id = review.product.id

        if not (request.user.is_staff and request.user.has_perm("products.delete_review")) and review.user != request.user:
            messages.warning(request, "You are not authorized to delete this review.", "alert-warning")
        else:
            review.delete()
            messages.success(request, "Review deleted successfully!", "alert-success")
    except Review.DoesNotExist:
        messages.error(request, "Review not found.", "alert-danger")

    return redirect("products:detail_product", product_id=product_id)
