from django import forms
from .models import Contact

#Creating form class
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields ="__all__"