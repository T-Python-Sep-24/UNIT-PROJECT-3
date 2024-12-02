from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    about = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='media/images/', default="media/images/profile_image.webp", blank=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.user.username}"

class Roll(models.Model):
    ROLE_CHOICES = [
        ('Manager', 'Manager'),
        ('Team Member', 'Team Member'),
    ]
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    users = models.ManyToManyField(User, related_name='roles')

    def __str__(self):
        return self.name

