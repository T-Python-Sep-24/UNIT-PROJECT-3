from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Testimonial
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


from organization.models import Opportunity

def homepage(request):
    all_opportunities = Opportunity.objects.all()
    return render(request, 'main/homepage.html', {'all_opportunities': all_opportunities})



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

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Profile

def register_volunteer(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, role='volunteer')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register_volunteer.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def dashboard(request):
    try:
        profile = request.user.profile
        if profile.role == 'organization':
            return render(request, 'organization/dashboard.html', {'profile': profile})
        elif profile.role == 'volunteer':
            return render(request, 'volunteers/dashboard.html', {'profile': profile})
        else:
            return render(request, 'main/dashboard.html', {'profile': profile})
    except AttributeError:
        messages.error(request, "Your profile is incomplete. Please contact support.")
        return redirect('main:homepage')
