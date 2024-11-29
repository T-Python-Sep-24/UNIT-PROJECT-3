from django import forms
from .models import Opportunity

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['title', 'description', 'location', 'time_commitment', 'required_skills', 'organization']
        widgets = {
            'required_skills': forms.CheckboxSelectMultiple(),
        }
