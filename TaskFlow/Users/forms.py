from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about', 'roll', 'photo']  # Only fields from Profile model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['roll'].choices = Profile.ROLE_CHOICES  # Dynamically populate roles
