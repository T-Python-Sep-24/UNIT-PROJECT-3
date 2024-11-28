from django.shortcuts import render, redirect
from django.http import HttpRequest , HttpResponse
from django.contrib import messages
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from .models import Employee , Customer

def employee_sign_up_view(request:HttpRequest):
    
    if request.method == "POST": 
        new_user = User.objects.create_user(username=request.POST["username"],email=request.POST["email"],password=request.POST["password"],first_name=request.POST["first_name"], last_name=request.POST["last_name"] )
        new_user.save() 
        employee_user = Employee(user=new_user,job_title=request.POST["job_title"],id_number= request.POST["id_number"])
        employee_user.save()
        messages.success( request,"Employee account created successfully." , "alert-success")
    
        return redirect("users:sign_in_view")
    return render(request , "users/employee_signup.html")

def customer_sign_up_view(request:HttpRequest):
    
    if request.method == "POST": 
        new_user = User.objects.create_user(username=request.POST["username"],email=request.POST["email"],password=request.POST["password"],first_name=request.POST["first_name"], last_name=request.POST["last_name"] )
        new_user.save() 
        customer_user = Customer(user=new_user,phone_number=request.POST["phone_number"])
        customer_user.save()
        messages.success( request,"Customer account created successfully." , "alert-success")
    
        return redirect("users:sign_in_view")
    return render(request , "users/customer_signup.html")

def sign_in_view(request:HttpRequest): 
    
    if request.method == "POST": 
        user = authenticate(request ,username=request.POST["username"] , password=request.POST["password"])

        if user: 
            login(request , user)
            messages.success(request, "logged in successfuly!" , "alert-success")
            return redirect("main:home_view")
        else:
            messages.error(request, "Invalid username or password. Please try again.", "alert-danger") 

    return render(request, "users/sign_in.html")


def logout_view(request:HttpRequest):
    logout(request)
    messages.success(request, "You have been logged out successfully.", "alert-success")
    return redirect("main:home_view")