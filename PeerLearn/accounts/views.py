from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def sign_up(request: HttpRequest):
    if request.method == "POST":
        try:
            new_user = User.objects.create_user(username=request.POST["username"], email=request.POST["email"], first_name=request.POST["first_name"], last_name=request.POST["last_name"], password=request.POST["password"])
            new_user.save()
            messages.success(request, "User created successfully", "alert-success")
            return redirect("accounts:sign_in")
        except Exception as e:
            messages.error(request, "Ther is an error. Please Try again later", "alert-danger")
            print(e)

    return render(request, "accounts/signup.html")



def sign_in(request: HttpRequest):
    if request.method == "POST":
        # get username and password from form
        username = request.POST["username"]
        password = request.POST["password"]
        # authenicate the user
        user = authenticate(request, username=username, password=password)

        # check if user authinicated
        if user is not None:   # we can use (if user): both works
            messages.success(request, "Login successfully", "alert-success")
            login(request, user)
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "Wrong credinitials", "alert-warning")

    return render(request, "accounts/signin.html")



def log_out(request: HttpRequest):
    logout(request)
    messages.success(request, "logged out successfully", "alert-warning")

    return redirect("main:home_view")