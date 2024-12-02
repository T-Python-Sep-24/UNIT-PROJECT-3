from django import forms
from .models import Organization, Opportunity


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'description', 'website', 'location']


class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['title', 'description', 'location', 'skills_required', 'start_date', 'end_date']
