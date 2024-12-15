from django import forms
from .models import Profile, Roll

class ProfileForm(forms.ModelForm):
    roles = forms.ModelChoiceField(queryset=Roll.objects.all(), required=False, label="Assign Role")

    class Meta:
        model = Profile
        fields = ['email', 'about', 'photo']

    def save(self, commit=True):
        profile = super().save(commit=False)
        role = self.cleaned_data.get("roles")
        if role:
            role.users.add(profile.user)
        if commit:
            profile.save()
        return profile
