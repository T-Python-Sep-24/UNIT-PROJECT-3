from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login , logout
from .models import UserProfile
from .forms import UserProfileForm, UserSkillsForm, VolunteerSignUpForm ,CompanySignUpForm



# View to Edit Profile
@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to dashboard after saving
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'users/edit_profile.html', {'form': form})


# View to Edit Skills
@login_required
def edit_skills(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserSkillsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to dashboard after saving
    else:
        form = UserSkillsForm(instance=profile)
    return render(request, 'users/edit_skills.html', {'form': form})


# Dashboard View
@login_required
def dashboard(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the dashboard after saving
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'users/dashboard.html', {
        'form': form,
        'profile': user_profile
    })


# Volunteer Registration View
def register_volunteer(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = VolunteerSignUpForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.is_volunteer = True
            profile.save()
            login(request, user)  # Log in the user after registration
            return redirect('dashboard')  # Redirect to the dashboard
    else:
        user_form = UserCreationForm()
        profile_form = VolunteerSignUpForm()

    return render(request, 'users/register_volunteer.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def register_company(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = CompanySignUpForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.is_organization = True
            profile.save()
            login(request, user)  # Log the user in after registration
            return redirect('dashboard')  # Redirect to the dashboard
    else:
        user_form = UserCreationForm()
        profile_form = CompanySignUpForm()
    return render(request, 'users/register_company.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})
from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout
