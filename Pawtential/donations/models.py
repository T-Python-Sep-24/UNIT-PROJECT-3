from django.db import models
from django.contrib.auth.models import User
from accounts.models import Shelter

# Create your models here.

class DonationRequest(models.Model):
    DONATION_TYPE_CHOICES = [
        ('food', 'Food'),
        ('supplies', 'Supplies'),
        ('medical', 'Medical'),
        ('other', 'Other'),
    ]
    
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='donation_requests')  
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPE_CHOICES)
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)     
    description = models.TextField(blank=True, null=True)
    date_requested = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False) 

    def __str__(self):
        return f"Donation Request for {self.shelter.name} - {self.donation_type}"
    
    def city(self):
        return self.shelter.address
    
    def check_fulfilled(self):
        if self.total_donated >= self.amount_requested:
            self.fulfilled = True
            self.save()

class Donation(models.Model):
    DONATION_METHOD_CHOICES = [
        ('cash', 'Cash Donation'),
        ('supplies', 'Supplies Donation'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'Bank Transfer'),
        ('apple_pay', 'Apple Pay'),
        ('paypal', 'PayPal'),
    ]
    
    donation_request = models.ForeignKey(DonationRequest, on_delete=models.CASCADE, related_name='donations') 
    donor_name = models.CharField(max_length=255, blank=True, null=True) 
    donation_type = models.CharField(max_length=20, choices=DONATION_METHOD_CHOICES)  
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    shipping_company = models.CharField(max_length=255, blank=True, null=True)  
    tracking_number = models.CharField(max_length=255, blank=True, null=True) 
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True) 
    date_donated = models.DateTimeField(auto_now_add=True)
    donation_status = models.CharField(max_length=50, default='pending') 
    
    def __str__(self):
        return f"{self.donor_name if self.donor_name else 'Anonymous'} - {self.donation_type} ({self.amount} SAR)"
