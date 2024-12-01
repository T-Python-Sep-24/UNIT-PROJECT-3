from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    ROLE_CHOICES = [
        ('Manager', 'Manager'),
    ]
    name = models.CharField(max_length=255)
    roll = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Manager')
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_projects")
    members = models.ManyToManyField(User, related_name="assigned_projects" , blank=True)

    def __str__(self):
        return self.name

