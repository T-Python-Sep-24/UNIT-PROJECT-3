from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="images/avatars/", default="images/avatars/a.png")
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Budget field
    
    def __str__(self):
        return f'{self.user.username} Profile'
    