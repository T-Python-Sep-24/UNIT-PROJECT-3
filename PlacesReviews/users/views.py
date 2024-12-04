from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from places.models import Place, Bookmark
from django.contrib import messages
from django.http import HttpRequest, Http404
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from .models import Profile
from django.db import transaction



def sign_up(request):
    """
    Handle user registration with a custom form.
    
    If the form is valid, the user is saved and redirected to the login page.
    Displays error messages for invalid submissions.
    
    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Render 'users/register.html' with the form.
    """
    try:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Registration successful!")
                return redirect('users:signin')  # After registration, redirect to login page
           
        else:
            form = CustomUserCreationForm()
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {e}")
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})




def user_profile_view(request, username):
    """
    Display a user's profile page with their published places.

    Args:
        request: HttpRequest object.
        username: Username of the profile to display.

    Returns:
        HttpResponse: Render 'users/profile.html' with user details and places.
    """
    try:
        
        profile_user = User.objects.filter(username=username).first()  

        if not profile_user:
            
            messages.error(request, f"User with username '{username}' not found.")
            profile_user, places, can_add_place = None, [], False
        else:
            places = Place.objects.filter(author=profile_user)
            can_add_place = request.user.is_authenticated and request.user == profile_user
    except Exception as e:
        messages.error(request, f"An error occurred while fetching the profile: {e}")
        profile_user, places, can_add_place = None, [], False

    context = {
        'profile_user': profile_user,
        'places': places,
        'can_add_place': can_add_place,
    }
    return render(request, 'users/profile.html', context)




@login_required
def user_bookmarks_view(request):
    """
    Display all places bookmarked by the logged-in user.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Render 'users/user_bookmarks.html' with bookmarks.
    """
    try:
        bookmarks = Bookmark.objects.filter(user=request.user).select_related('place')
    except Bookmark.DoesNotExist:
        bookmarks = []
        messages.warning(request, "No bookmarks found.")
    except Exception as e:
        bookmarks = []
        messages.error(request, f"An error occurred: {e}")
    
    return render(request, 'users/user_bookmarks.html', {'bookmarks': bookmarks})

def sign_in(request: HttpRequest):
    """
    Handle user login and authenticate credentials.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Render 'users/signin.html' for login page.
    """
    if request.method == "POST":
        # Authenticate the user
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            # Login the user
            login(request, user)
            messages.success(request, "Logged in successfully!", "alert-success")
            # Redirect to the next page or homepage
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "Invalid credentials. Please try again.", "alert-danger")
    
    return render(request, "users/login.html")

def log_out(request: HttpRequest):
    """
    Logout the user and redirect to the next page.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Redirect to the next page or homepage after logout.
    """
    logout(request)
    messages.success(request, "Logged out successfully!", "alert-warning")
    
    return redirect(request.GET.get("next", "/"))


