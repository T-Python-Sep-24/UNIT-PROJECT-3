from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Profile
# Create your views here.


def signup_view(request: HttpRequest):

    if request.method == "POST":

        try:
            with transaction.atomic():
                new_user = User.objects.create_user(username=request.POST["username"],password=request.POST["password"],email=request.POST["email"], first_name=request.POST["first_name"], last_name=request.POST["last_name"])
                new_user.save()

                profile = Profile(user=new_user, about=request.POST["about"],budget=request.POST.get("budget",0.0), avatar=request.FILES.get("avatar", Profile.avatar.field.get_default()))
                profile.save()

            messages.success(request, "Registered User Successfuly", "alert-success")
            return redirect("accounts:signin_view")
        
        except IntegrityError as e:
            messages.error(request, "Please choose another username", "alert-danger")
        except Exception as e:
            messages.error(request, "Couldn't register user. Try again", "alert-danger")
            print(e)
    
    return render(request, "accounts/signup.html")


def signin_view(request:HttpRequest):

    if request.method=="POST":
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user:
            login(request,user)
            messages.success(request,f"welcome {user.username}","alert-success")
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request,"field to login to your account","alert-danger")
    return render(request,"accounts/signin.html")


def log_out(request:HttpRequest):
    username=request.user.username
    logout(request)
    messages.success(request,f'See you soon {username}',"alert-dark")
    return redirect('main:home_view')


def profile_view(request:HttpRequest,user_name):
    
    try:
        user=User.objects.get(username=user_name)
        tickets=user.ticket_set.all()
        if not Profile.objects.filter(user=user).first():
            user_profile=Profile(user=user)
            user_profile.save()
        
    except Exception as e :
        messages.error(request,f"What are you doing {e}",'alert-warning')
        return redirect('main:home_view')
    
    
    page_number = request.GET.get("page", 1)
    paginator = Paginator(tickets, 2)
    tickets_page = paginator.get_page(page_number)

    return render(request,"accounts/profile.html",context={'user':user,'tickets':tickets_page})


def update_profile_view(request:HttpRequest):
    if not request.user.is_authenticated:
        messages.warning(request,"you have to login first!","alert-warning")
        return redirect("accounts:signin_view")
    if request.method=='POST':
        try:
           with transaction.atomic():
            user:User =request.user
            
            user.first_name=request.POST['first_name']
            user.last_name=request.POST['last_name']
            user.email=request.POST['email']
            user.save()
            profile:Profile=user.profile
            profile.about=request.POST['about']
            profile.avatar=request.FILES.get('avatar',profile.avatar)
            profile.save()
            
           messages.success(request,"Profile Updated successfully !","alert-success")
           return redirect('accounts:profile_view',user_name=user.username)
        except Exception as e:
            print(e)
            messages.error(request,"We couldn't update your profile","alert-danger")

    return render(request,'accounts/update_profile.html')

def update_budget_view(request:HttpRequest):

    if not request.user.is_authenticated:
        messages.warning(request,"you have to login first!","alert-warning")
        return redirect("accounts:signin_view")
    
    if request.method == 'POST':
        try:
            profile:Profile=request.user.profile
            budget=float(profile.budget )
            new_budget= budget + float(request.POST['budget'])
            profile.budget=new_budget
            profile.save()
            messages.success(request,"budget Updated successfully !","alert-success")
            return redirect('accounts:profile_view',user_name=request.user.username)
        except Exception as e:
            print(e)

    return render(request,'accounts/update_budget.html')
    
