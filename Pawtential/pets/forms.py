from django import forms
from .models import Pet

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'image', 'species', 'breed', 'age', 'health_status', 'adoption_status']
