from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import IndividualUser, Shelter
from django.contrib.auth.decorators import login_required
from .forms import ShelterProfileForm ,IndividualUserForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful! Welcome')
            return redirect('main:home_view')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')

def register_individual_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username:
            messages.error(request, "Username is required.")
            return render(request, 'accounts/individual_registration.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return render(request, 'accounts/individual_registration.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/individual_registration.html')

        user = User.objects.create_user(username=username, email=email, password=password)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number', '')
        bio = request.POST.get('bio', '')
        birth_date = request.POST.get('birth_date', None)
        profile_picture = request.FILES.get('profile_picture', None)

        individual_user = IndividualUser(
            user=user,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            bio=bio,
            birth_date=birth_date,
            profile_picture=profile_picture
        )
        individual_user.save()

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('accounts:login') 

    return render(request, 'accounts/individual_registration.html')

def register_shelter_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken. Please choose a different one.")
            return render(request, 'accounts/shelter_registration.html')


        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/shelter_registration.html')

        user = User.objects.create_user(username=username, email=email, password=password)

        shelter_name = request.POST.get('shelter_name')
        phone_number_shelter = request.POST.get('phone_number_shelter')
        address = request.POST.get('address')
        license_number = request.POST.get('license_number')
        bio = request.POST.get('bio', '')
        profile_picture = request.FILES.get('profile_picture_shelter', None)

        shelter = Shelter(
            user=user,
            name=shelter_name,
            phone_number=phone_number_shelter,
            address=address,
            license_number=license_number,
            bio=bio,
            profile_picture=profile_picture
        )
        shelter.save()

        messages.success(request, "Shelter account created successfully. Please log in.")
        return redirect('accounts:login')

    return render(request, 'accounts/shelter_registration.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect('main:home_view')

def individual_profile(request):
    profile = IndividualUser.objects.get(user=request.user )
    return render(request, 'profile/individual_profile.html', {'profile': profile})

def edit_individual_profile(request):
    profile = IndividualUser.objects.get(user=request.user)

    if request.method == 'POST':
        form = IndividualUserForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:individual_profile')  
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = IndividualUserForm(instance=profile)

    return render(request, 'profile/individual_edit_profile.html', {'form': form})

def shelter_profile(request):
    shelter_profile = Shelter.objects.get(user=request.user)
    return render(request, 'profile/shelter_profile.html', {'profile': shelter_profile})

def edit_shelter_profile(request):
    profile = Shelter.objects.get(user=request.user)

    if request.method == 'POST':
        form = ShelterProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            form.save()  
            return redirect('accounts:shelter_profile')  
    else:
        form = ShelterProfileForm(instance=profile)

    return render(request, 'profile/shelter_edit_profile.html', {'form': form})