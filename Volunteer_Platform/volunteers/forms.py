from django import forms
from .models import Volunteer, Application


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['bio', 'skills', 'profile_picture']


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']

from django import forms
from django.contrib.auth.models import User
from .models import Volunteer

class VolunteerRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    class Meta:
        model = Volunteer
        fields = ['bio', 'skills', 'profile_picture']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        volunteer = super().save(commit=False)
        volunteer.user = user
        if commit:
            volunteer.save()
            self.save_m2m()  # Save ManyToMany fields like skills
        return volunteer
