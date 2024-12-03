from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Organization, Opportunity
from .forms import  OpportunityForm

# Organization-related views
def organization_list(request):
    organizations = Organization.objects.all()
    return render(request, 'organization/organization_list.html', {'organizations': organizations})

# Opportunity-related views
def opportunity_list(request):
    opportunities = Opportunity.objects.all()
    return render(request, 'organization/opportunity_list.html', {'opportunities': opportunities})

def opportunity_detail(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    return render(request, 'organization/opportunity_detail.html', {'opportunity': opportunity})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OpportunityForm

@login_required
def add_opportunity(request):
    if request.user.profile.role != 'organization':
        messages.error(request, "You do not have permission to add opportunities.")
        return redirect('main:homepage')

    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.organization = request.user
            opportunity.save()
            messages.success(request, "Opportunity added successfully!")
            return redirect('organization:opportunity_list')
    else:
        form = OpportunityForm()

    return render(request, 'organization/add_opportunity.html', {'form': form})
