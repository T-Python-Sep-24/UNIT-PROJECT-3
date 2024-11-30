from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from organizations.models import Opportunity
from accounts.models import OrganizationProfile
from accounts.models import VolunteerProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Q

# Create your views here.

def all_opportunities_view(request:HttpRequest):
    
    search_query = request.GET.get('search', '').strip()
    city_filter = request.GET.get('city', '').strip()
    focus_industry = request.GET.get('focus_industry', '').strip()

    cities = Opportunity.objects.values_list('city', flat=True).distinct()

    opportunities = Opportunity.objects.all()

    if search_query:
        opportunities = opportunities.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if city_filter:
        opportunities = opportunities.filter(city__icontains=city_filter)

    if focus_industry:
        opportunities = opportunities.filter(focus_industry__iexact=focus_industry)

    context = {'opportunities': opportunities, 'cities': cities,}

    
    return render(request, 'opportunities/all_opportunities.html', context)



def opportunity_detail_view(request, id):

    opportunity = get_object_or_404(Opportunity, id=id)

    organization = opportunity.organization
    
    return render(request, 'opportunities/opportunity_details.html', {'opportunity': opportunity, 'organization': organization})




def update_opportunity_view(request, opportunity_id):
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)

    if request.user != opportunity.organization.organization_user:
        messages.error(request, "You are not authorized to update this opportunity.")
        return redirect("opportunities:opportunity_detail_view", id=opportunity_id)

    if request.method == "POST":
        opportunity.name = request.POST.get("name")
        opportunity.city = request.POST.get("city")
        opportunity.location = request.POST.get("location")
        opportunity.time = request.POST.get("time")
        opportunity.event_type = request.POST.get("event_type")
        opportunity.focus_industry = request.POST.get("focus_industry")
        opportunity.education_level_required = request.POST.get("education_level_required")
        opportunity.description = request.POST.get("description")
        opportunity.number_of_volunteers_needed = request.POST.get("number_of_volunteers_needed")
        
        if request.FILES.get("image"):
            opportunity.image = request.FILES.get("image")

        opportunity.save()
        messages.success(request, "Opportunity updated successfully!")
        return redirect('opportunities:opportunity_detail_view',  id=opportunity.id)

    return render(request, 'opportunities/update_opportunity.html', {'opportunity': opportunity})



@login_required
def delete_opportunity_view(request: HttpRequest, opportunity_id: int):
    opportunity = get_object_or_404(Opportunity, pk=opportunity_id)

    if request.user != opportunity.organization.organization_user:
        messages.error(request, "You are not authorized to delete this opportunity.")
        return redirect("opportunities:opportunity_detail_view", id=opportunity_id)

    opportunity.delete()
    messages.success(request, "Opportunity deleted successfully!")
    return redirect("opportunities:all_opportunities_view")





@login_required
def apply_to_opportunity_view(request, id):
    
    opportunity = get_object_or_404(Opportunity, id=id)
    
    has_volunteer_profile = hasattr(request.user, "volunteerprofile")
    
    return render(request, 'opportunities/opportunity_details.html', {'opportunity': opportunity, 'has_volunteer_profile': has_volunteer_profile})

