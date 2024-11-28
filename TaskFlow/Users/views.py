from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError, transaction
# Rest-API
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import fetch_roles  # Assuming fetch_roles() is defined in utils.py
# Models
from django.contrib.auth.models import User
from .models import Profile
# Forms
from .forms import ProfileForm

def sign_up(request: HttpRequest):
    if request.method == "POST":
        try:
            with transaction.atomic():
                # Create the new user
                new_user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password"],
                    email=request.POST["email"]
                )
                new_user.save()
                # Get roll value and handle it properly
                roll = request.POST.get("roll")
                if not roll:
                    messages.error(request, "Role is required", "alert-danger")
                    raise Exception("Role not provided")
                # Create a profile for the user
                profile = Profile.objects.create(
                    user=new_user,
                    about=request.POST.get("about", ""),  # Default to empty string if 'about' is not provided
                    roll=roll,  # Ensure `roll` exists in your model or as a valid value
                    photo=request.FILES.get("photo",Profile.photo.field.get_default())
                )
                profile.save()
            messages.success(request, "Registered user successfully", "alert-success")
            return redirect("Users:sign_in")
        except IntegrityError:
            messages.error(request, "Please choose another username", "alert-danger")
        except Exception as e:
            messages.error(request, "Couldn't register user. Try again", "alert-danger")
            print(f"Error: {e}")
    return render(request, "users/signup.html", {})


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

def fetch_roles():
    url = "https://login.auth0.com/api/v2/roles"  
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN', 
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        return response.json()  # Return roles as a list of dictionaries
    except requests.exceptions.RequestException as e:
        print(f"Error fetching roles: {e}")
        return []


class RoleListView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        roles = fetch_roles()
        if roles:
            formatted_roles = [{"id": role["id"], "name": role["name"]} for role in roles]
            return Response(formatted_roles)
        return Response({"error": "Unable to fetch roles"}, status=500)


class AssignRoleView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, profile_id):
        try:
            profile = Profile.objects.get(id=profile_id)
            role_name = request.data.get('role_name')
            if not role_name:
                return Response({"error": "Role name is required"}, status=400)
            roles = fetch_roles()
            valid_roles = [role["name"] for role in roles]
            if role_name not in valid_roles:
                return Response({"error": "Invalid role name"}, status=400)
            profile.roll = role_name
            profile.save()
            return Response({"message": f"Role '{role_name}' assigned to user '{profile.user.username}'"})
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)
        except Exception as e:
            return Response({"error": f"An error occurred: {e}"}, status=500)


def log_out(request: HttpRequest):
    logout(request)
    messages.success(request, "logged out successfully", "alert-warning")
    return redirect(request.GET.get("next", "/"))