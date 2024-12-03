from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Testimonial, Profile
from organization.models import Opportunity
from .forms import OpportunityFilterForm


# Homepage with filters, sorting, and testimonials
def homepage(request):
    form = OpportunityFilterForm(request.GET or None)
    opportunities = Opportunity.objects.all()

    # Filter by category
    category = request.GET.get('category')
    if category:
        opportunities = opportunities.filter(category=category)

    # Filter by opportunity type
    opportunity_type = request.GET.get('opportunity_type')
    if opportunity_type:
        opportunities = opportunities.filter(opportunity_type=opportunity_type)

    # Sort opportunities
    sort_by = request.GET.get('sort_by', 'title')  # Default sorting by title
    if sort_by in ['title', 'category', 'date_created']:  # Ensure sorting by valid fields
        opportunities = opportunities.order_by(sort_by)

    # Fetch testimonials
    testimonials = Testimonial.objects.all().order_by('-created_at')[:10]  # Limit to 10 recent testimonials

    return render(request, 'main/homepage.html', {
        'form': form,
        'opportunities': opportunities,
        'testimonials': testimonials,
        'sort_by': sort_by,
    })



# About page
def about(request):
    return render(request, 'main/about.html')


# Contact page
def contact(request):
    return render(request, 'main/contact.html')


# Dashboard view for logged-in users
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


# Logout view
def CustomLogoutView(request):
    logout(request)
    return redirect('main:homepage')


# Register organization
def register_organization(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.role = 'organization'  # Assign organization role
            user.profile.save()
            messages.success(request, 'Your organization account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'main/register_organization.html', {'form': form})


# Register volunteer
def register_volunteer(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, role='volunteer')
            messages.success(request, 'Your volunteer account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register_volunteer.html', {'form': form})
