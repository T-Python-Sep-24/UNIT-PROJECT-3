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
    amount_remaining = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)    
    description = models.TextField(blank=True, null=True)
    date_requested = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False) 

    def __str__(self):
        return f"Donation Request for {self.shelter.name} - {self.donation_type}"
    
    def city(self):
        return self.shelter.address
    
    def check_fulfilled(self):
        total_donated = self.donations.aggregate(models.Sum('amount'))['amount__sum'] or 0
        if total_donated >= self.amount_requested:
            self.fulfilled = True
        else:
            self.fulfilled = False
        self.save()
    
    def update_remaining_amount(self):
        if self.amount_requested is None:
            return 
        
        total_donated = self.donations.aggregate(models.Sum('amount'))['amount__sum'] or 0
        self.amount_remaining = self.amount_requested - total_donated
        self.check_fulfilled()  
        self.save()

class Donation(models.Model):
    DONATION_METHOD_CHOICES = [
        ('cash', 'Cash Donation'),
        ('supplies', 'Supplies Donation'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'Bank Transfer'),
        ('apple_pay', 'Apple Pay'),
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
    payment_proof = models.FileField(upload_to='payment_proofs/', blank=True, null=True)

    
    def __str__(self):
        return f"{self.donor_name if self.donor_name else 'Anonymous'} - {self.donation_type} ({self.amount} SAR)"

    def is_bank_transfer(self):
        return self.payment_method == 'bank_transfer'
    
    def check_payment_proof(self):
        if self.is_bank_transfer() and not self.payment_proof:
            return False 
        return True 
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  
        self.donation_request.update_remaining_amount() 
