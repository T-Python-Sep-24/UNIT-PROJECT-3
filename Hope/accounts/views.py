from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import OrganizationProfile
from .models import VolunteerProfile


# Create your views here.

def organization_signup_view(request:HttpRequest):
    
    if request.method == "POST":
        organization_name = request.POST.get("organization_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        description = request.POST.get("description")

        if not organization_name or not email or not password:
            messages.error(request, "All fields are required!")
            return redirect("accounts:organization_signup_view")

        if User.objects.filter(username=organization_name).exists():
            messages.error(request, "Organization name already taken!")
            return redirect("accounts:organization_signup_view")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use!")
            return redirect("accounts:organization_signup_view")
        
        organization_user = User.objects.create_user(username=organization_name, email=email, password=password)
        organization_user.save()

        OrganizationProfile.objects.create(organization_user=organization_user, organization_name=organization_name, description=description,)

        messages.success(request, "Account created successfully! Please login.")
        return redirect("accounts:login_view")
    
    return render(request, 'accounts/organization_signup.html')




def volunteer_signup_view(request:HttpRequest):

    if request.method == "POST":
        volunteer_name = request.POST.get("volunteer_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        description = request.POST.get("description")

        if not volunteer_name or not email or not password:
            messages.error(request, "All fields are required!")
            return redirect("accounts:volunteer_signup_view")

        if User.objects.filter(username=volunteer_name).exists():
            messages.error(request, "Name already taken!")
            return redirect("accounts:volunteer_signup_view")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use!")
            return redirect("accounts:volunteer_signup_view")
        
        volunteer_user = User.objects.create_user(username=volunteer_name, email=email, password=password)
        volunteer_user.save()

        VolunteerProfile.objects.create(volunteer_user=volunteer_user, full_name=volunteer_name, bio=description,)

        messages.success(request, "Account created successfully! Please log in.")
        return redirect("accounts:login_view")
    
    return render(request, 'accounts/volunteer_signup.html')




def login_view(request:HttpRequest):

    if request.method == "POST":
        username_or_email = request.POST.get("email_or_username")
        password = request.POST.get("password")

        user = authenticate(request, username=username_or_email if User.objects.filter(username=username_or_email).exists() else User.objects.filter(email=username_or_email).first(), password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect(request.GET.get("next", "/"))  
        
        else:
            messages.error(request, "Invalid username/email or password!")
            return redirect("accounts:login_view")
    
    return render(request, 'accounts/login.html')




def logout_view(request:HttpRequest):

    logout(request)
    messages.success(request, "You logged out successfully!")

    return redirect(request.GET.get("next", "/"))
    
