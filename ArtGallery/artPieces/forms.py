from django import forms
from .models import ArtPiece

# Form for ArtPiece model
class ArtPieceForm(forms.ModelForm):
    class Meta:
        model = ArtPiece
        fields ="__all__"
