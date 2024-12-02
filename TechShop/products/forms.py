from django import forms
from .models import Product

# Create a form for adding and editing products
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__" 
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter product name"}),
            'description': forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Enter product description"}),
            'price': forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter product price"}),
            'image': forms.ClearableFileInput(attrs={"class": "form-control"}),
            'category': forms.Select(attrs={"class": "form-control"}),
        }
