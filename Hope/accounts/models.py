from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class OrganizationProfile(models.Model):
    ORGANIZATION_TYPE_CHOICES = [
        ('Non-Profit', 'Non-Profit'),
        ('Corporate', 'Corporate'),
        ('Government', 'Government'),
        ('Startup', 'Startup'),
    ]

    FOCUS_INDUSTRY_CHOICES = [
        ('Medical', 'Medical'),
        ('Entertainment', 'Entertainment'),
        ('Education', 'Education'),
        ('Environment', 'Environment'),
        ('Technology', 'Technology'),
    ]

    
    organization_user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True) 
    organization_logo = models.ImageField(upload_to="organization_logos/", blank=True, null=True, default="organization_logos/default_logo.png")
    organization_type = models.CharField(
        max_length=100, choices=ORGANIZATION_TYPE_CHOICES, blank=True, null=True
    )

    industry_focus_area = models.CharField(
        max_length=100, choices=FOCUS_INDUSTRY_CHOICES, blank=True, null=True
    )

    def __str__(self):
        return self.organization_name
    


class VolunteerProfile(models.Model):
    class EducationLevel(models.TextChoices):
        HIGH_SCHOOL = "High School", "High School"
        ASSOCIATE = "Associate's Degree", "Associate's Degree"
        BACHELORS = "Bachelor's Degree", "Bachelor's Degree"
        MASTERS = "Master's Degree", "Master's Degree"
        DOCTORATE = "Doctorate", "Doctorate"


    volunteer_user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True, default="profile_pictures/default_profile.png")
    skills = models.CharField(max_length=255, blank=True, null=True)
    applied_opportunities = models.ManyToManyField("organizations.Opportunity", related_name="applicants", blank=True,)
    experience = models.TextField(blank=True, null=True)
    education_level = models.CharField(
        max_length=20,
        choices=EducationLevel.choices,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.full_name    

