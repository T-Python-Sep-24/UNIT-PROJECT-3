from django import forms
from .models import Artist

# Form for Artist model
class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields ="__all__"
