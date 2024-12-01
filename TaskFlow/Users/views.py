from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError, transaction
# Models
from django.contrib.auth.models import User
from .models import Profile
from projects.models import Project
from tasks.models import Task
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



def sign_in(request: HttpRequest):
    if request.method == "POST":
        # Checking user credentials
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        print(user)
        if user:
            # Log in the user
            login(request, user)
            messages.success(request, "Logged in successfully", "alert-success")
            # Redirect to the dashboard with the username
            return redirect("Users:dashboard_view", username=user.username)
        else:
            messages.error(request, "Please try again. Your credentials are wrong", "alert-danger")

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
    return render(request, 'users/profile.html', {"user": user})



@login_required
def update_user_profile(request: HttpRequest):
    if request.method == "POST":
        try:
            with transaction.atomic():
                user = request.user

                # Update user fields
                user.first_name = request.POST.get("first_name", user.first_name)
                user.last_name = request.POST.get("last_name", user.last_name)
                user.email = request.POST.get("email", user.email)
                user.save()

                # Update profile fields
                profile = user.profile
                profile.about = request.POST.get("about", profile.about)
                profile.roll = request.POST.get("roll", profile.roll)
                if "photo" in request.FILES:
                    profile.photo = request.FILES["photo"]
                profile.save()

            messages.success(request, "Profile updated successfully!", "alert-success")
        except Exception as e:
            messages.error(request, "An error occurred while updating your profile.", "alert-danger")
            print(e)

    user = request.user
    profile = user.profile

    return render(request, "users/update_profile.html", {
        "user": user,
        "profile": profile,
    })

@login_required
def dashboard_view(request, username):
    user = get_object_or_404(User, username=username)
    if user.profile.roll in ["Manager", "Team Lead"]:
        projects = Project.objects.filter(created_by=user) | Project.objects.filter(members=user)
        tasks = Task.objects.filter(project__in=projects)
        context = {
            'user': user,
            'projects': projects,
            'tasks': tasks,
        }
        return render(request, 'users/dashboard.html', context)



    

def log_out(request: HttpRequest):
    logout(request)
    messages.success(request, "logged out successfully", "alert-warning")
    return redirect(request.GET.get("next", "/"))