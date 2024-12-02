from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Volunteer, Application
from organization.models import Opportunity
from .forms import VolunteerForm, ApplicationForm


@login_required
def profile(request):
    volunteer = get_object_or_404(Volunteer, user=request.user)
    return render(request, 'volunteers/profile.html', {'volunteer': volunteer})


def browse_opportunities(request):
    opportunities = Opportunity.objects.all()
    return render(request, 'volunteers/browse_opportunities.html', {'opportunities': opportunities})


@login_required
def application_list(request):
    volunteer = get_object_or_404(Volunteer, user=request.user)
    applications = volunteer.applications.all()
    return render(request, 'volunteers/application_list.html', {'applications': applications})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Volunteer, Application
from organization.models import Opportunity
from .forms import ApplicationForm

@login_required
def apply_for_opportunity(request, opportunity_id):
    # Retrieve the opportunity
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)

    # Check if the user has a Volunteer profile
    try:
        volunteer = request.user.volunteer
    except Volunteer.DoesNotExist:
        messages.error(request, "You need a Volunteer profile to apply for opportunities.")
        return redirect('volunteers:opportunity_list')

    # Handle the application process
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.volunteer = volunteer
            application.opportunity = opportunity
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect('volunteers:application_list')
    else:
        form = ApplicationForm()

    return render(request, 'volunteers/apply_for_opportunity.html', {'form': form, 'opportunity': opportunity})
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'volunteers/dashboard.html')


from django.shortcuts import render, redirect
from .forms import VolunteerRegistrationForm

def register_as_volunteer(request):
    if request.method == 'POST':
        form = VolunteerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main:homepage')  # Redirect to homepage or login
    else:
        form = VolunteerRegistrationForm()
    return render(request, 'volunteers/register.html', {'form': form})
