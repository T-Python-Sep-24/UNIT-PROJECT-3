from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Place(models.Model):
    CATEGORY_CHOICES = [
        ('Restaurant', 'Restaurant'),
        ('Entertainment', 'Entertainment'),
        ('Cafe', 'Cafe'),
        ('Museum', 'Museum'),
        ('Park', 'Park'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    photo = models.ImageField(upload_to='places/')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'place')
    
