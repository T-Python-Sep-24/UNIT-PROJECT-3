from django import forms
from .models import Donation

class DonationForm(forms.Form):
    donor_name = forms.CharField(required=False, max_length=100)
    donation_type = forms.ChoiceField(choices=[('monetary', 'Monetary Donation'), ('supplies', 'Supplies Donation')], required=True)
    
    amount = forms.DecimalField(required=False, max_digits=10, decimal_places=2, min_value=0.01)
    payment_method = forms.ChoiceField(choices=[('bank_transfer', 'Bank Transfer'), ('apple_pay', 'Apple Pay')], required=False)
    
    shipping_company = forms.CharField(required=False, max_length=100)
    tracking_number = forms.CharField(required=False, max_length=100)
    
    payment_proof = forms.FileField(required=False)