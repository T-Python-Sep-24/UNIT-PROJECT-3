from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from main.models import Language
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError, transaction
from partners.models import Request,Partner
from django.core.paginator import Paginator
from .models import Profile

# Create your views here.


def sign_up(request: HttpRequest): 
   
    languages=Language.objects.all()

    if request.method == "POST":
        try:
            with transaction.atomic():
                new_user = User.objects.create_user(username=request.POST["username"],password=request.POST["password"],email=request.POST["email"])
                new_user.save()  
                native_language = Language.objects.get(id=request.POST["native_language"])
                target_language = Language.objects.get(id=request.POST["target_language"])

                profile=Profile(user=new_user,about=request.POST["about"],
                                avatar=request.FILES.get("avatar",Profile.avatar.field.get_default()),
                                native_language=native_language,
                                target_language=target_language,
                                gender=request.POST["gender"])
                profile.save()
               
                messages.success(request, "Registered User Successfuly", "alert-success")
                return redirect("accounts:sign_in")
        except Exception as e:
            messages.error(request, "Couldn't register user. Try again", "alert-danger")
            print(e)
    

    return render(request, "accounts/signup.html",{"languages":languages,"GenderChoices":Profile.GenderChoices.choices})



def sign_in(request:HttpRequest):

    if request.method == "POST":

        #checking user credentials
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        print(user)
        if user:
            #login the user
            login(request, user)
            messages.success(request, "Hello, "+ user.username, "alert-success")
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "Please try again. You credentials are wrong", "alert-danger")


    #
    return render(request, "accounts/signin.html")


def log_out(request: HttpRequest):
    username = request.user.username
    logout(request)
    messages.success(request, "See you later, "+ username+" (logged out successfully)", "alert-warning")

    return redirect(request.GET.get("next", "/"))



def user_profile_view(request,user_name):
    try:
        user=User.objects.get(username=user_name)
       
        if  request.user.is_authenticated:
            sent_requests = request.user.sent_requests.all()
            received_requests=user.received_requests.all()
            partners=request.user.partners.all()
            partnered_users = user.partnered_users.all()
            print( partners)
            #check the request users
            is_requested=False
            accept_req=False
            if sent_requests.exists() and received_requests.exists():     
                    is_requested=True
            
        else:
             sent_requests=[]
             received_requests=[]
             partners=[]
             partnered_users=[]
             is_requested=False
        #if dosent have profile
        #if not Profile.objects.filter(user=user).first():
         #   new_profile = Profile(user=user)
        #    new_profile.save()   
    except Exception as e:
        print(e)
        return render(request,"404.html")

    return render(request,"accounts/profile.html",{"user":user,"sent_requests":sent_requests,
                                                   "is_requested":is_requested,"received_requests":received_requests,
                                                   "partners":partners,
                                                   "partnered_users":partnered_users})


def update_profile_view(request):
        if not request.user.is_authenticated:
            messages.warning(request,"only rigisted user can update thier profile","alert-warning")
            return redirect("accounts:sign_in")
        
       
        languages=Language.objects.all()

        if request.method =="POST":
                try:
                    with transaction.atomic():
                        user:User = request.user
                        user.username = request.POST["username"]
                        user.email = request.POST["email"]
                        if "password" in request.POST and request.POST["password"].strip() != "":
                            print( request.POST["password"]) 
                            user.set_password(request.POST["password"])  
                            user.save()      
                        else:
                            user.save()                       
                        native_language = Language.objects.get(id=request.POST["native_language"])
                        target_language = Language.objects.get(id=request.POST["target_language"])

                        profile:Profile = user.profile
                        profile.about = request.POST["about"]
                        profile.native_language = native_language
                        profile.target_language = target_language
                        profile.gender = request.POST["gender"]
                        if "avatar" in request.FILES: profile.avatar = request.FILES["avatar"]
                        profile.save()

                    messages.success(request, "updated profile successfuly", "alert-success")
                except Exception as e:
                    messages.error(request, "Couldn't update profile", "alert-danger")
                    print(e)

        return render(request,"accounts/update_profile.html",{"GenderChoices":Profile.GenderChoices.choices,"languages":languages})




def all_partners_profiles_view(request):
    all_partners=Profile.objects.filter(role='partner')
    languages=Language.objects.all()
    if "search" in request.GET and len(request.GET["search"]) >= 1:
        all_partners = all_partners.filter(user__username__icontains=request.GET["search"])

    if "filter_by_native" in request.GET and request.GET["filter_by_native"]:
        all_partners = all_partners.filter(native_language__id=request.GET["filter_by_native"])

    if "filter_by_target" in request.GET and request.GET.get("filter_by_target"):
        all_partners = all_partners.filter(target_language__id=request.GET["filter_by_target"])
    
    p=Paginator(all_partners,6)
    page=request.GET.get('page',1)
    all_partners_list=p.get_page(page)
    return render(request,'accounts/all_profiles.html',{"all_partners":all_partners_list,"languages":languages})