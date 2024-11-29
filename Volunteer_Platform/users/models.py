from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_volunteer = models.BooleanField(default=False)
    is_organization = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    skills = models.ManyToManyField('Skill', blank=True)

class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
