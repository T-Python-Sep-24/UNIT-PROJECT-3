from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donor_name', 'donation_type', 'amount', 'shipping_company', 'tracking_number']

    amount = forms.DecimalField(required=False, min_value=0.01, decimal_places=2, label="Amount to Donate")
    shipping_company = forms.CharField(required=False, max_length=255, label="Shipping Company")
    tracking_number = forms.CharField(required=False, max_length=255, label="Tracking Number")

    def __init__(self, *args, **kwargs):
        super(DonationForm, self).__init__(*args, **kwargs)
        if self.instance.donation_type == 'supplies':
            self.fields['shipping_company'].required = True
            self.fields['tracking_number'].required = True
        elif self.instance.donation_type == 'monetary':
            self.fields['amount'].required = True
            self.fields['shipping_company'].required = False
            self.fields['tracking_number'].required = False
