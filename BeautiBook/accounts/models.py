from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    role = models.OneToOneField(User ,on_delete=models.CASCADE)
    about_user = models.TextField(blank=True)
    is_artist = models.BooleanField(default=False)
    def __str__(self):
        return f"Profile {self.role.username}"