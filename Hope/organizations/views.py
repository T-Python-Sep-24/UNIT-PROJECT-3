from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Opportunity
from accounts.models import OrganizationProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q





# Create your views here.

def all_organizations_view(request:HttpRequest):

    search_query = request.GET.get('search', '').strip()

    organizations = OrganizationProfile.objects.all()

    if search_query:
        organizations = organizations.filter(
            Q(organization_name__icontains=search_query) |
            Q(industry_focus_area__icontains=search_query)
        )

    return render(request, 'organizations/all_organizations.html', {'organizations': organizations})


@login_required
def add_opportunity_view(request:HttpRequest):

    if not hasattr(request.user, 'organizationprofile'):
        messages.error(request, "You must be logged in as an organization to add opportunities.")
        return redirect('main:main_view')

    if request.method == "POST":
        organization = OrganizationProfile.objects.get(organization_user=request.user)
        name = request.POST.get("name")
        city = request.POST.get("city")
        location = request.POST.get("location")
        time = request.POST.get("time")
        event_type = request.POST.get("event_type")
        focus_industry = request.POST.get("focus_industry")
        description = request.POST.get("description")
        education_level_required = request.POST.get("education_level_required")
        number_of_volunteers_needed = request.POST.get("number_of_volunteers_needed")
        image = request.FILES.get("image")

        Opportunity.objects.create(
            organization=organization,
            name=name,
            city=city,
            location=location,
            time=time,
            event_type=event_type,
            focus_industry=focus_industry,
            description=description,
            education_level_required=education_level_required,
            number_of_volunteers_needed=number_of_volunteers_needed,
            image=image
        )
        messages.success(request, "Opportunity added successfully!")
        return redirect("main:main_view")

    return render(request, "organizations/add_opportunity.html")
