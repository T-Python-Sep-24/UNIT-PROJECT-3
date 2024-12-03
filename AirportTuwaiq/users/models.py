from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    job_title = models.CharField(max_length=100)
    id_number = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.job_title}"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username