from django import forms
from .models import Place

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'description', 'city', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter place name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city name'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
