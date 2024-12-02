from django import forms
from .models import Organization, Opportunity


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'description', 'website', 'location', 'image']

from django import forms
from .models import Opportunity  # Ensure you import your Opportunity model

class OpportunityForm(forms.ModelForm):
    SOFT_SKILLS_CHOICES = [
        ('communication', 'Communication'),
        ('teamwork', 'Teamwork'),
        ('problem_solving', 'Problem Solving'),
    ]

    HARD_SKILLS_CHOICES = [
        ('coding', 'Coding'),
        ('design', 'Design'),
        ('data_analysis', 'Data Analysis'),
    ]

    OTHER_SKILLS_CHOICES = [
        ('none', 'None'),
        ('project_management', 'Project Management'),
        ('marketing', 'Marketing'),
        ('writing', 'Writing'),
    ]

    soft_skills = forms.MultipleChoiceField(
        choices=SOFT_SKILLS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Soft Skills"
    )

    hard_skills = forms.MultipleChoiceField(
        choices=HARD_SKILLS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Hard Skills"
    )

    other_skills = forms.ChoiceField(
        choices=OTHER_SKILLS_CHOICES,
        required=False,
        label="Other Skills"
    )

    image = forms.ImageField(
        required=False,
        label="Upload Image"
    )

    class Meta:
        model = Opportunity
        fields = ['title', 'description', 'location', 'start_date', 'end_date', 'soft_skills', 'hard_skills', 'other_skills', 'image']