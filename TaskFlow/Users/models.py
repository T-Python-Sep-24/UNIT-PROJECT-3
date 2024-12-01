from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    about = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='media/images/', default="media/images/profile_image.webp")
    password = models.CharField(max_length=128)

    
    def __str__(self):
        return f"{self.user.username}"