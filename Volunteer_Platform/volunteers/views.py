from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Volunteer
from .forms import VolunteerRegistrationForm, VolunteerEditForm
from organization.models import Opportunity

@login_required
def dashboard(request):
    return render(request, 'volunteers/dashboard.html')

def register_as_volunteer(request):
    if request.method == 'POST':
        form = VolunteerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('volunteers:dashboard')
    else:
        form = VolunteerRegistrationForm()
    return render(request, 'volunteers/register.html', {'form': form})

@login_required
def edit_profile(request):
    volunteer = get_object_or_404(Volunteer, user=request.user)
    if request.method == 'POST':
        form = VolunteerEditForm(request.POST, instance=volunteer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('volunteers:dashboard')
    else:
        form = VolunteerEditForm(instance=volunteer)
    return render(request, 'volunteers/edit_profile.html', {'form': form})

def browse_opportunities(request):
    opportunities = Opportunity.objects.all()
    return render(request, 'volunteers/browse_opportunities.html', {'opportunities': opportunities})


def browse_opportunities(request):
    opportunities = Opportunity.objects.all()
    return render(request, 'volunteers/browse_opportunities.html', {'opportunities': opportunities})

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from organization.models import Opportunity
from .models import Volunteer, VolunteerApplication

@login_required
def apply_for_opportunity(request, opportunity_id):
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)

    # Check if the user has a Volunteer profile
    try:
        volunteer = request.user.volunteer  # Ensure the logged-in user has a Volunteer profile
    except Volunteer.DoesNotExist:
        messages.error(request, "You must register as a volunteer before applying for opportunities.")
        return redirect('volunteers:dashboard')

    # Check if the user has already applied for this opportunity
    if VolunteerApplication.objects.filter(volunteer=volunteer, opportunity=opportunity).exists():
        messages.error(request, "You have already applied for this opportunity.")
    else:
        # Create the application
        VolunteerApplication.objects.create(volunteer=volunteer, opportunity=opportunity)
        messages.success(request, "Application submitted successfully!")

    return redirect('volunteers:dashboard')
