from django import forms
from .models import Profile, Roll

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about',  'photo']  



class RollForm(forms.ModelForm):
    class Meta:
        model = Roll
        fields = ['name', 'users']
