from django.db import models

class Profile(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField()
    about = models.TextField(blank=True, null=True)
    roll = models.CharField(max_length=50)  # Store the role as a string
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Role name (e.g., Manager, Team Member)

    def __str__(self):
        return self.name


