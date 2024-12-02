from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Testimonial
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def homepage(request):
    testimonials = Testimonial.objects.all().order_by('-created_at')[:3]
    return render(request, 'main/homepage.html', {'testimonials': testimonials})


def about(request):
    return render(request, 'main/about.html')


def contact(request):
    return render(request, 'main/contact.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    if request.user.profile.role == 'organization':
        return render(request, 'organization/dashboard.html')
    elif request.user.profile.role == 'volunteer':
        return render(request, 'volunteers/dashboard.html')
    else:
        return render(request, 'main/dashboard.html')  


def register(request):
    pass


def CustomLogoutView(request):
    logout(request)
    return redirect('main:homepage')




def register_organization(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.role = 'organization'  # Assuming a role field in the profile
            user.profile.save()
            messages.success(request, 'Your organization account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'main/register_organization.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')  # Redirect to login after successful registration
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    
    # Render the form for both GET requests and invalid POST requests
    return render(request, 'main/register.html', {'form': form})

