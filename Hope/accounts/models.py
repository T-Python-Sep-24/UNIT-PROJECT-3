from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class OrganizationProfile(models.Model):
    organization_user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.organization_name
    


class VolunteerProfile(models.Model):
    volunteer_user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    skills = models.CharField(max_length=255, blank=True, null=True)
    experience = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name    

