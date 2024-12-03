from django import forms
from django.contrib.auth.models import User

class OrganizationRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    logo = forms.ImageField(required=False, label="Upload Logo")  # Added logo field

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'logo']  # Include logo in fields

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    

class UserRegistrationForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('volunteer', 'Volunteer'),
        ('organization', 'Organization'),
    ]

    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Select Role")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    


    from django import forms
from organization.models import Opportunity

class OpportunityFilterForm(forms.Form):
    CATEGORY_CHOICES = [
        ('technical', 'Technical'),
        ('health', 'Health'),
        ('education', 'Education'),
        ('environment', 'Environment'),
    ]
    OPPORTUNITY_TYPE_CHOICES = [
        ('remote', 'Remote'),
        ('onsite', 'Onsite'),
    ]

    category = forms.ChoiceField(
        choices=[('', 'All Categories')] + CATEGORY_CHOICES,
        required=False,
        label='Category'
    )
    opportunity_type = forms.ChoiceField(
        choices=[('', 'All Types')] + OPPORTUNITY_TYPE_CHOICES,
        required=False,
        label='Opportunity Type'
    )
