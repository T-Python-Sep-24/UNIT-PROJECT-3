from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about', 'avatar']

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-bordered'}), label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-bordered'}), label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")
class ChildUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-bordered'}), label="Password")

    class Meta:
        model = User
        fields = ['username', 'email']

class ChildProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = []