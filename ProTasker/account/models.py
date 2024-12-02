from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar= models.ImageField(upload_to="images/avatar/", default="images/avatar.webp")
    about=models.TextField(blank=True)
   
    def __str__(self) -> str:
        return f"Profle {self.user.username}"
    