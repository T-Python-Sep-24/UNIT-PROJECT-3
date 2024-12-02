from django.db import models
from django.contrib.auth.models import User
from pets.models import Pet

# Create your models here.

class AdoptionRequest(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    pet = models.ForeignKey(Pet , related_name='adoption_requests',on_delete=models.CASCADE)
    user = models.ForeignKey(User , related_name='adoption_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES , default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comments = models.TextField(blank=True, null=True)
    comment_by_approver = models.TextField(null=True, blank=True) 

    class Meta:
        unique_together = ['pet', 'user']
        
    def __str__(self):
        return f"Adoption Request by {self.user.username} for {self.pet.name} ({self.status})"