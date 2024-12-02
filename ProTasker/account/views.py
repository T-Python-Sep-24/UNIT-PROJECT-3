from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Profile
from tasks.models import Task
from project.models import Project

# Create your views here.
def sign_up(request: HttpRequest):

    if request.method == "POST":
        try:
           
            if User.objects.filter(username=request.POST["username"]).exists():
                messages.error(request, "Username already exists. Please choose another one.", "alert-danger")
                return render(request, "main/sign_up.html")

    
            new_user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password"],
                email=request.POST.get("email", ""),
                first_name=request.POST.get("first_name", ""),
                last_name=request.POST.get("last_name", ""),
               
            )
            new_user.save()

         
            avatar = request.FILES.get("avatar", Profile.avatar.field.get_default())

           
            profile = Profile(user=new_user, avatar=avatar,about=request.POST["about"])
            profile.save()

        
            messages.success(request, "Registered User Successfully", "alert-success")
            return redirect("account:sign_in")

        except Exception as e:
            messages.error(request, f"Error: {str(e)}", "alert-danger")
            print("Error during sign-up:", e)

    return render(request, "main/sign_up.html")


def sign_in(request: HttpRequest):
    if request.method == "POST":
        print("Received POST request with data:", request.POST)
        user = authenticate(
            request, 
            username=request.POST.get("username"), 
            password=request.POST.get("password")
        )
        if user:
            print("Authentication successful for user:", user)
            login(request, user)
            messages.success(request, "Logged in successfully", "alert-success")
            return redirect("main:home_view")
        else:
            print("Authentication failed.")
            messages.error(request, "Try again", "alert-warning")

    return render(request, "main/sign_in.html")



def log_out(request:HttpRequest):
    logout(request)
    messages.success(request,"Logout successfully","alert-success")

    return redirect("main:home_view")



def user_profile_view(request: HttpRequest, user_name):
    try:

        user = User.objects.get(username=user_name)
        profile = user.profile  
        print(user.profile.avatar)
    except User.DoesNotExist:
        messages.error(request, "User not found.", "alert-danger")
        return redirect("account:user_profile_view") 

    return render(request, "main/profile.html", {"profile": profile,"user":user })


def update_user_profile(request:HttpRequest):
    if not request.user.is_authenticated:
        messages.error(request,"Only registerd users can update this prfile","alert-warning")
        return redirect("account:sign_in")
   

    if request.method == "POST":
        user:User = request.user

        user.first_name=request.POST["first_name"]
        user.last_name=request.POST["last_name"]
        user.email=request.POST["email"]
        user.save()

        profile:Profile = user.profile
        profile.avatar=request.FILES.get("avatar",profile.avatar)
        profile.about=request.POST["about"]
        profile.save()
        messages.success(request,"updated successfuly","alert-success")
       
        

    return render(request,"main/update_profile.html")