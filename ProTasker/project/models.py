from django.contrib.auth.models import User
from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=50, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')])
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_projects') 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name