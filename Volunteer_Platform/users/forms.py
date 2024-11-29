from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'skills']

class VolunteerSignUpForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'skills']

class CompanySignUpForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio']

from django import forms
from .models import UserProfile, Skill

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'skills']

class UserSkillsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['skills']
        widgets = {
            'skills': forms.CheckboxSelectMultiple
        }
