from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Profile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username','first_name' , 'last_name', 'email', 'password1', 'password2', 'photo']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        if self.cleaned_data.get('photo'):
            user.profile.photo = self.cleaned_data['photo']
            user.profile.save()

        return user

    

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email')
