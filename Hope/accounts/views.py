from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import OrganizationProfile
from .models import VolunteerProfile
from django.db import IntegrityError, transaction
from django.urls import reverse
from organizations.models import Opportunity



# Create your views here.

@transaction.atomic
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

        login(request, organization_user)
        return redirect(reverse("accounts:organization_profile", kwargs={"username": organization_user.username}))

    
    return render(request, 'accounts/organization_signup.html')



@transaction.atomic
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

        login(request, volunteer_user)
        return redirect(reverse("accounts:volunteer_profile", kwargs={"username": volunteer_user.username}))
    
    return render(request, 'accounts/volunteer_signup.html')




def login_view(request:HttpRequest):

    if request.method == "POST":
        username_or_email = request.POST.get("email_or_username")
        password = request.POST.get("password")

        user = None

        if User.objects.filter(username=username_or_email).exists():
            user = authenticate(request, username=username_or_email, password=password)

        elif User.objects.filter(email=username_or_email).exists():
            user_obj = User.objects.filter(email=username_or_email).first()

            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password)
                
        if user is not None:
            login(request, user)
            return redirect("main:main_view")  
        

            #I Don't need this testing code
            if hasattr(user, "organizationprofile"):
                return redirect(reverse("main:organization_profile", kwargs={"username": user.username}))
            
            elif hasattr(user, "volunteerprofile"):
                return redirect(reverse("accounts:volunteer_profile", kwargs={"username": user.username}))
            
            else:
                messages.error(request, "Profile type not found.")
                return redirect("accounts:login_view")
            
        else:
            messages.error(request, "Invalid username/email or password!")
            return redirect("accounts:login_view")
    
    return render(request, 'accounts/login.html')




def logout_view(request:HttpRequest):

    logout(request)
    messages.success(request, "You logged out successfully!")

    return redirect(request.GET.get("next", "/"))



@login_required
def organization_profile(request:HttpRequest, username):

    user = get_object_or_404(User, username=username)
    profile, created = OrganizationProfile.objects.get_or_create(organization_user=user)

    if created:
        messages.info(request, "Welcome! Please complete your organization profile.")

    if request.method == "POST":
        profile.organization_name = request.POST.get("organization_name", profile.organization_name)
        profile.description = request.POST.get("description", profile.description)
        profile.website_url = request.POST.get("website_url", profile.website_url)
        profile.organization_type = request.POST.get("organization_type", profile.organization_type)
        profile.industry_focus_area = request.POST.get("industry_focus_area", profile.industry_focus_area)

        if request.FILES.get("organization_logo"):
            profile.organization_logo = request.FILES.get("organization_logo")
        
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("accounts:organization_profile", username=user.username)
    

    return render(request, 'accounts/organization_profile.html', {'profile': profile})




def organization_update_profile(request:HttpRequest, username):

    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(OrganizationProfile, organization_user=user)

    if request.method == "POST":
        profile.organization_name = request.POST.get("organization_name", profile.organization_name)
        profile.description = request.POST.get("description", profile.description)
        profile.website_url = request.POST.get("website_url", profile.website_url)
        profile.organization_type = request.POST.get("organization_type", profile.organization_type)
        profile.industry_focus_area = request.POST.get("industry_focus_area", profile.industry_focus_area)
        profile.email = request.POST.get("email", profile.email) 

        if request.FILES.get("organization_logo"):
            profile.organization_logo = request.FILES.get("organization_logo")

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("accounts:organization_profile", username=username)

    return render(request,'accounts/organization_update_profile.html', {'profile': profile})



@login_required
def volunteer_profile(request:HttpRequest, username):

    user = get_object_or_404(User, username=username)
    profile, created = VolunteerProfile.objects.get_or_create(volunteer_user=user)

    if created:
        messages.info(request, "Welcome! Please complete your profile.")

    applied_opportunities = profile.applied_opportunities.all()    
    
    return render(request, 'accounts/volunteer_profile.html', {'profile': profile, 'applied_opportunities': applied_opportunities})



def volunteer_update_profile(request:HttpRequest, username):

    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(VolunteerProfile, volunteer_user=user)

    if request.method == "POST":
        profile.full_name = request.POST.get("full_name", profile.full_name)
        profile.bio = request.POST.get("bio", profile.bio)
        profile.skills = request.POST.get("skills", profile.skills)
        profile.experience = request.POST.get("experience", profile.experience)
        profile.education_level = request.POST.get("education_level", profile.education_level)

        if request.FILES.get("profile_picture"):
            profile.profile_picture = request.FILES.get("profile_picture")

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("accounts:volunteer_profile", username=user.username)

    return render(request,'accounts/volunteer_update_profile.html', {'profile': profile})