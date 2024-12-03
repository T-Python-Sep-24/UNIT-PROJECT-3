from django import forms
from django.contrib.auth.models import User
from .models import Volunteer


class VolunteerRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

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
        label="Soft Skills"
    )
    hard_skills = forms.MultipleChoiceField(
        choices=HARD_SKILLS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Hard Skills"
    )
    other_skills = forms.ChoiceField(
        choices=OTHER_SKILLS_CHOICES,
        required=False,
        label="Other Skills"
    )

    class Meta:
        model = Volunteer
        fields = ['bio', 'profile_picture']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        volunteer = super().save(commit=False)
        volunteer.user = user

        # Save skills as JSON fields
        volunteer.soft_skills = self.cleaned_data.get('soft_skills', [])
        volunteer.hard_skills = self.cleaned_data.get('hard_skills', [])
        volunteer.other_skills = self.cleaned_data.get('other_skills', '')

        if commit:
            volunteer.save()
        return volunteer

from django import forms
from .models import Volunteer



class VolunteerEditForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['bio', 'skills', 'profile_picture']
