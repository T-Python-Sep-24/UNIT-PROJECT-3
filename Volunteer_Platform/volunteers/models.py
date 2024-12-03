from django.db import models
from django.contrib.auth.models import User
from organization.models import Opportunity  # Adjust import based on your project structure


class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='volunteer')
    bio = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='volunteer_profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username




class VolunteerApplication(models.Model):
    volunteer = models.ForeignKey('volunteers.Volunteer', on_delete=models.CASCADE, related_name='applications')
    opportunity = models.ForeignKey('organization.Opportunity', on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.volunteer.user.username} applied for {self.opportunity.title}"