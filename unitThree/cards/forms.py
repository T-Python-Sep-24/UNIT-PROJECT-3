from django import forms
from .models import Flashcard, Folder

class CardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['question', 'answer']

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'description','category'] 
