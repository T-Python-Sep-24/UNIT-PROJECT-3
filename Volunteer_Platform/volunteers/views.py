from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from .models import Volunteer, VolunteerApplication
from .forms import VolunteerRegistrationForm, VolunteerEditForm
from organization.models import Opportunity

# Dashboard view
@login_required
def dashboard(request):
    try:
        volunteer = request.user.volunteer
        applications = VolunteerApplication.objects.filter(volunteer=volunteer)
    except Volunteer.DoesNotExist:
        volunteer = None
        applications = []

    return render(request, 'volunteers/dashboard.html', {
        'applications': applications,
    })

# Register as a volunteer
def register_as_volunteer(request):
    if request.method == 'POST':
        form = VolunteerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            Volunteer.objects.create(user=user, bio='', profile_picture=None)  # Create Volunteer profile
            return redirect('volunteers:dashboard')
    else:
        form = VolunteerRegistrationForm()
    return render(request, 'volunteers/register.html', {'form': form})

# Edit volunteer profile
@login_required
def edit_profile(request):
    try:
        volunteer = request.user.volunteer  # Attempt to fetch the associated Volunteer profile
    except Volunteer.DoesNotExist:
        # Handle the case where no Volunteer is associated with the user
        messages.error(request, "You do not have a volunteer profile.")
        return redirect('volunteers:register_as_volunteer')  # Redirect to the registration page

    if request.method == 'POST':
        form = VolunteerEditForm(request.POST, request.FILES, instance=volunteer)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('volunteers:dashboard')
    else:
        form = VolunteerEditForm(instance=volunteer)

    return render(request, 'volunteers/edit_profile.html', {'form': form})
# Browse opportunities
def browse_opportunities(request):
    opportunities = Opportunity.objects.all()
    return render(request, 'volunteers/browse_opportunities.html', {'opportunities': opportunities})

# Apply for an opportunity
@login_required
def apply_for_opportunity(request, opportunity_id):
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)

    try:
        volunteer = request.user.volunteer
    except Volunteer.DoesNotExist:
        messages.error(request, "You must register as a volunteer before applying for opportunities.")
        return redirect('volunteers:dashboard')

    if VolunteerApplication.objects.filter(volunteer=volunteer, opportunity=opportunity).exists():
        messages.error(request, "You have already applied for this opportunity.")
    else:
        VolunteerApplication.objects.create(volunteer=volunteer, opportunity=opportunity)
        messages.success(request, "Application submitted successfully!")

    return redirect('volunteers:dashboard')

# Delete volunteer profile
@login_required
def delete_profile(request):
    try:
        volunteer = request.user.volunteer
        volunteer.delete()
        messages.success(request, "Your profile has been deleted successfully.")
    except Volunteer.DoesNotExist:
        messages.error(request, "You do not have a profile to delete.")

    return redirect('main:homepage')
