from django.db import models
from django.contrib.auth.models import User
from project.models import Project

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200) 
    description = models.TextField()  
    priority_choices = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    priority = models.CharField(max_length=10, choices=priority_choices, default='medium')  
    status_choices = [
        ('to_do', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='to_do') 
    due_date = models.DateField() 
    completion_date = models.DateField(null=True, blank=True)  
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')  
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  

    def __str__(self):
        return self.title


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
