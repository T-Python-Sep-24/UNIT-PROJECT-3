from django import forms
from .models import Screening

class ScreeningForm(forms.ModelForm):
    class Meta:
        model = Screening
        fields = ['movie', 'theater', 'showtime', 'price']
