from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Opportunity(models.Model):
    EVENT_TYPE_CHOICES = [
        ('Profit', 'Profit'),
        ('Non-Profit', 'Non-Profit'),
    ]

    FOCUS_INDUSTRY_CHOICES = [
        ('Medical', 'Medical'),
        ('Entertainment', 'Entertainment'),
        ('Education', 'Education'),
        ('Environment', 'Environment'),
        ('Technology', 'Technology'),
        
    ]

    EDUCATION_LEVEL_CHOICES = [
        ('None', 'No Education Required'),
        ('High School', 'High School Diploma'),
        ('Bachelor', 'Bachelor’s Degree'),
        ('Master', 'Master’s Degree'),
        ('PhD', 'PhD'),
    ]

    organization = models.ForeignKey("accounts.OrganizationProfile", on_delete=models.CASCADE, related_name='opportunities')
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    location = models.TextField()
    time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    focus_industry = models.CharField(max_length=50, choices=FOCUS_INDUSTRY_CHOICES)
    description = models.TextField()
    education_level_required = models.CharField(max_length=50, choices=EDUCATION_LEVEL_CHOICES)
    number_of_volunteers_needed = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to="opportunity_images/", blank=True, null=True, default="opportunity_images/default_image.png")


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']