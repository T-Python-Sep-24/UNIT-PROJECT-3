from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from .models import Profile, Bookmark
from funds_app.models import Fund

# Create your views here.


def sign_up(request: HttpRequest):

    if request.method == "POST":
        try:
            with transaction.atomic():
                new_user = User.objects.create_user(
                    first_name = request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    email = request.POST['email'],
                    password = request.POST['password'],
                    username = request.POST['username'],
                )
                new_user.save()

                profile = Profile(
                    user = new_user,
                    about = request.POST['about'],
                    avatar = request.FILES.get("avatar", Profile._meta.get_field("avatar").get_default()),
                )

                profile.save()

            messages.success(request, f'{new_user.username} Account was created Successfully', 'alert-success')
            return redirect('accounts:sign_in')
        except IntegrityError as ie:
            print(ie)
            messages.error(request, 'This username is taken, please try another one', 'alert-danger')
        except Exception as e:
            print(e)
            messages.error(request, 'error in creating your account', 'alert-danger')
    return render(request, 'signup.html')


def sign_in(request: HttpRequest):

    if request.method == "POST":
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            messages.success(request, f'{user.username} Signed in Successfully', 'alert-success')
            return redirect(request.GET.get('next', '/'))
        else:
            messages.error(request, 'Username or password is wrong, please try again', 'alert-danger')
    return render(request, 'signin.html')


def log_out(request: HttpRequest):


    logout(request)
    messages.success(request, 'logged out successfully, See You later', 'alert-success')
    return redirect(request.GET.get('next', '/'))


def profile_view(request: HttpRequest, user_name):

    user = User.objects.get(username=user_name)
    if not Profile.objects.filter(user = user).first():
        new_profile = Profile(user=user)
        new_profile.save()
    profile: Profile = user.profile
    # profile = Profile.objects.get(user=user)


    return render(request, 'profile.html', context={'user':user })


def update_profile_view(request: HttpRequest):

    if not request.user.is_authenticated:
        messages.error(request, "Sign in to update your profile","alert-warning")
        return redirect("accounts:sign_in")

    if request.method == "POST":
        try:
            with transaction.atomic():
                # update and  the user model
                user: User = request.user
                print(user.last_name)
                print(request.POST['last_name'])
                user.username = request.POST['username']
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.email = request.POST['email']
                user.save()
                # as long as updating the profile model
                profile:Profile = user.profile
                profile.about = request.POST['about']
                if 'avatar' in request.FILES: profile.avatar = request.FILES['avatar']
                profile.save()

            messages.success(request, f'Profile was Updated Successfully', 'alert-success')
            return redirect('accounts:profile_view', user_name=request.user.username)

        except Exception as e:
            print(e)
            messages.error(request, 'error in updating your profile ', 'alert-danger')
    return render(request, 'update_profile.html')