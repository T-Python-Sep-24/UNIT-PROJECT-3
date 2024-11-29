from django import forms
from .models import IndividualUser, Shelter


class IndividualUserForm(forms.ModelForm):
    class Meta:
        model = IndividualUser
        fields = ['first_name', 'last_name', 'username', 'email', 'birth_date', 'phone_number', 'bio', 'profile_picture']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
class ShelterProfileForm(forms.ModelForm):
    class Meta:
        model = Shelter
        fields = ['name', 'phone_number', 'address', 'license_number', 'bio', 'profile_picture'] 

