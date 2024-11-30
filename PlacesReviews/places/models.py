from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Place(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to='places/')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'place')
    
