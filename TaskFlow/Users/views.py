from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError, transaction
# Models
from django.contrib.auth.models import User
from .models import Profile
# Forms
from .forms import ProfileForm

def sign_up(request):
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES)
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if profile_form.is_valid():
            try:
                with transaction.atomic():
                    # Create the User
                    user = User.objects.create_user(username=username, email=email, password=password)

                    # Create the Profile
                    profile = profile_form.save(commit=False)
                    profile.user = user  # Link the profile to the user
                    profile.save()

                    messages.success(request, "Registered user successfully", "alert-success")
                    return redirect("Users:sign_in")
            except Exception as e:
                messages.error(request, f"Error: {e}", "alert-danger")
        else:
            messages.error(request, "Form is invalid. Please correct the errors.", "alert-danger")
    else:
        profile_form = ProfileForm()

    return render(request, "users/signup.html", {"form": profile_form})



def sign_in(request:HttpRequest):

    if request.method == "POST":

        #checking user credentials
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        print(user)
        if user:
            #login the user
            login(request, user)
            messages.success(request, "Logged in successfully", "alert-success")
            return redirect(request.GET.get("main:index_view", "/"))
        else:
            messages.error(request, "Please try again. You credentials are wrong", "alert-danger")

    return render(request, "users/signin.html")

def user_profile_view(request:HttpRequest, user_name):
    try:
        user = User.objects.get(username=user_name)
        if not Profile.objects.filter(user=user).first():
            new_profile = Profile(user=user)
            new_profile.save()
        #profile:Profile = user.profile  
        #profile = Profile.objects.get(user=user)
    except Exception as e:
        print(e)
        return render(request,'main/404.html')
    return render(request, 'users/profile.html', {"user" : user})


@login_required
def update_user_profile(request: HttpRequest):
        profile = Profile.objects.get(user=request.user)
        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Your profile has been updated successfully.", "alert-success")
                return redirect("users:user_profile_view", user_name=request.user.username)  # Redirect to the profile view
            else:
                messages.error(request, "Please correct the errors below.", "alert-danger")
        else:
            form = ProfileForm(instance=profile)
        return render(request, "users/update_profile.html", {"form": form, "profile": profile})



def log_out(request: HttpRequest):
    logout(request)
    messages.success(request, "logged out successfully", "alert-warning")
    return redirect(request.GET.get("next", "/"))