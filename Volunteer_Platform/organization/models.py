from django.db import models
from django.contrib.auth.models import User
from main.models import Location


class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organization')
    name = models.CharField(max_length=255)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='organizations')
    image = models.ImageField(upload_to='organizations/images/', blank=True, null=True)

    def __str__(self):
        return self.name

from django.db import models

class Opportunity(models.Model):
    CATEGORY_CHOICES = [
        ('technical', 'Technical'),
        ('health', 'Health'),
        ('education', 'Education'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    opportunity_type = models.CharField(
        max_length=50,
        choices=[('remote', 'Remote'), ('in_person', 'In Person')]
    )
    image = models.ImageField(upload_to='opportunities/images/', blank=True, null=True)

    def __str__(self):
        return self.title
