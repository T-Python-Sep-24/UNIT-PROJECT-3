from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('Manager', 'Manager'),
        ('Team Lead', 'Team Lead'),
        ('Team Member', 'Team Member'),
        ('Client', 'Client'),
        ('Quality Assurance', 'QA'),
        ('Product Owner', 'Product Owner'),
        ('Stakeholder', 'Stakeholder'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    about = models.TextField(blank=True, null=True)
    roll = models.CharField(max_length=50, choices=ROLE_CHOICES)
    photo = models.ImageField(upload_to='media/images/', blank=True, null=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username