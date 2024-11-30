from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from places.models import Place, Bookmark
from django.contrib import messages
from django.http import HttpRequest
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView


def register_view(request):
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
    return render(request, 'users/register.html', {'form': form})


# User profile view
def user_profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    places = Place.objects.filter(author=profile_user)  # Get places published by this user

    # Check if the logged-in user matches the profile owner
    can_add_place = request.user.is_authenticated and request.user == profile_user

    context = {
        'profile_user': profile_user,
        'places': places,
        'can_add_place': can_add_place,
    }
    return render(request, 'users/profile.html', context)



class CustomLoginView(LoginView):
    def get_success_url(self):
        return f'/users/profile/{self.request.user.username}/'
    
@login_required
def user_bookmarks_view(request):
    """
    Display all places bookmarked by the logged-in user.
    """
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('place')
    return render(request, 'users/user_bookmarks.html', {'bookmarks': bookmarks})    