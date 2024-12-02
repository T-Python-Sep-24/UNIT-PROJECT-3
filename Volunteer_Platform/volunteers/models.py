from django.db import models
from django.contrib.auth.models import User


class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="volunteer")
    bio = models.TextField(blank=True, null=True)
    skills = models.ManyToManyField('main.Skill', blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Application(models.Model):
    volunteer = models.ForeignKey('volunteers.Volunteer', on_delete=models.CASCADE, related_name='applications')
    opportunity = models.ForeignKey('organization.Opportunity', on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending')
    date_applied = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.volunteer.user.username} - {self.opportunity.title}"
