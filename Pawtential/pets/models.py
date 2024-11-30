from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Pet(models.Model):

    HEALTH_CHOICES = [
        ('healthy', 'Healthy'),          
        ('sick', 'Sick'),                 
        ('treatment', 'Under Treatment'), 
    ]

    ADOPTION_CHOICES = [
        ('available', 'Available for Adoption'),
        ('adopted', 'Adopted'),
        ('not_available', 'Not Available for Adoption'),
    ]

    name = models.CharField(max_length=100) 
    image = models.ImageField(upload_to='pet_images/', blank=True, null=True) 
    species = models.CharField(max_length=150) 
    breed = models.CharField(max_length=50, blank=True, null=True)  
    age = models.FloatField() 
    health_status = models.CharField(max_length=20, choices=HEALTH_CHOICES, default='healthy') 
    adoption_status = models.CharField(max_length=20, choices=ADOPTION_CHOICES, default='available')  
    medical_history = models.TextField(blank=True, null=True)  
    location = models.CharField(max_length=255, blank=True, null=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')  
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name