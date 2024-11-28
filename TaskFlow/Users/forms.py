from django import forms
from .models import Profile, Role

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'about', 'roll', 'photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['roll'].queryset = Role.objects.all()  # Fetch roles dynamically
