from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from django.contrib import messages
from .models import Profile
from .forms import SignUpForm, ProfileForm, ChildUserForm, ChildProfileForm
from django.db.models import Count
from cards.models import Flashcard , Folder
from django.contrib.auth.decorators import login_required



# Create your views here.

def sign_up(request):
    if request.method == "POST":
        user_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    user = user_form.save(commit=False)
                    user.set_password(user_form.cleaned_data["password"])
                    user.save()

                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.user_type = 'parent'  # Default to parent
                    profile.save()

                    messages.success(request, "Registered successfully!")
                    return redirect("accounts:sign_in")
            except Exception as e:
                messages.error(request, "An error occurred during registration.")
                print(e)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        user_form = SignUpForm()
        profile_form = ProfileForm()

    return render(request, "accounts/signup.html", {"user_form": user_form, "profile_form": profile_form})



def update_user_profile(request: HttpRequest):
    if not request.user.is_authenticated:
        messages.warning(request, "Only registered users can update their profile", "alert-warning")
        return redirect("accounts:sign_in")

    if request.method == "POST":
        try:
            with transaction.atomic():
                user: User = request.user

                user.first_name = request.POST["first_name"]
                user.last_name = request.POST["last_name"]
                user.email = request.POST["email"]
                user.save()

                profile: Profile = user.profile
                profile.about = request.POST["about"]
                profile.twitch_link = request.POST["twitch_link"]
                if "avatar" in request.FILES:
                    profile.avatar = request.FILES["avatar"]

                if parent_username:
                    try:
                        parent_user = User.objects.get(username=parent_username)
                        profile.parent = parent_user
                    except User.DoesNotExist:
                        messages.error(request, "Parent user does not exist.", "alert-danger")
                        return render(request, "accounts/update_profile.html")
                else:
                    profile.parent = None

                profile.save()

            messages.success(request, "Profile updated successfully", "alert-success")
        except Exception as e:
            messages.error(request, "Couldn't update profile", "alert-danger")
            print(e)

    return render(request, "accounts/update_profile.html")  

    if request.method == "POST":

        try:
            with transaction.atomic():
                user:User = request.user

                user.first_name = request.POST["first_name"]
                user.last_name = request.POST["last_name"]
                user.email = request.POST["email"]
                user.save()

                profile:Profile = user.profile
                profile.about = request.POST["about"]
                profile.twitch_link = request.POST["twitch_link"]
                if "avatar" in request.FILES: profile.avatar = request.FILES["avatar"]
                profile.save()

            messages.success(request, "updated profile successfuly", "alert-success")
        except Exception as e:
            messages.error(request, "Couldn't update profile", "alert-danger")
            print(e)

    return render(request, "accounts/update_profile.html")



def sign_in(request:HttpRequest):

    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        print(user)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully", "alert-success")
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "Please try again. You credentials are wrong", "alert-danger")



    return render(request, "accounts/signin.html")


def log_out(request: HttpRequest):

    logout(request)
    messages.success(request, "logged out successfully", "alert-warning")

    return redirect(request.GET.get("next", "/"))

@login_required
def user_profile_view(request, user_name):
    user = get_object_or_404(User, username=user_name)
    profile = user.profile

    if profile.user_type == 'child' and request.user != user and request.user.profile.user_type != 'parent':
        messages.error(request, "You do not have permission to view this profile.")
        return redirect('cards:home_views') 

    context = {"user": user, "profile": profile}

    if profile.user_type == 'child' and request.user == user:
        flashcard_count = Flashcard.objects.filter(user=user).count()
        folder_count = Folder.objects.filter(user=user).count()
        context['flashcard_count'] = flashcard_count
        context['folder_count'] = folder_count

    if profile.user_type == 'parent' and request.user == user:
        children = Profile.objects.filter(parent=user).annotate(
            flashcard_count=Count('user__flashcards'),
            folder_count=Count('user__folders')
        )
        context['children'] = children

    return render(request, 'accounts/profile.html', context)
@login_required
def add_child_user(request):
    if not request.user.profile.user_type == 'parent':
        messages.error(request, "Only parents can add child users.")
        return redirect('home_views')

    if request.method == "POST":
        user_form = ChildUserForm(request.POST)
        profile_form = ChildProfileForm(request.POST)

        if user_form.is_valid():
            try:
                with transaction.atomic():
                    user = user_form.save(commit=False)
                    user.set_password(user_form.cleaned_data["password"])
                    user.save()

                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.user_type = 'child'
                    profile.parent = request.user
                    profile.save()

                    messages.success(request, "Child user added successfully!")
                    return redirect('accounts:user_profile', user_name=user.username)
            except Exception as e:
                messages.error(request, "An error occurred while adding the child user.")
                print(e)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        user_form = ChildUserForm()
        profile_form = ChildProfileForm()

    return render(request, "accounts/add_child_user.html", {"user_form": user_form})