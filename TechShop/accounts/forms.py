from django import forms
from .models import Profile, CartItem

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about']  


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']  
