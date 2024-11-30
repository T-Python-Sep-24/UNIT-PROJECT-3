from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from places.models import Place, Bookmark
from django.contrib import messages
from django.http import HttpRequest, Http404
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView


def register_view(request):
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
                return redirect('users:login')
            else:
                messages.error(request, "Please correct the error below.")
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
        profile_user = get_object_or_404(User, username=username)
        places = Place.objects.filter(author=profile_user)
        can_add_place = request.user.is_authenticated and request.user == profile_user
    except User.DoesNotExist:
        raise Http404("User not found.")
    except Exception as e:
        messages.error(request, f"An error occurred while fetching the profile: {e}")
        profile_user, places, can_add_place = None, [], False

    context = {
        'profile_user': profile_user,
        'places': places,
        'can_add_place': can_add_place,
    }
    return render(request, 'users/profile.html', context)


class CustomLoginView(LoginView):
    """
    Custom login view to redirect to the user's profile after successful login.

    Returns:
        str: URL of the user's profile page.
    """
    def get_success_url(self):
        try:
            return f'/users/profile/{self.request.user.username}/'
        except Exception as e:
            messages.error(self.request, f"An error occurred: {e}")
            return '/'

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
