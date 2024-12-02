from django.contrib.auth.models import User
from django.db import models
from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(
        max_length=50,
        choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')],
        default='Medium' 
    )
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_projects')
    team_members = models.ManyToManyField(User, related_name='projects', through='TeamMember', blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True) 
    status = models.CharField(
        max_length=50,
        choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed')],
        default='Not Started'
    )  

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=[('Leader', 'Leader'), ('Member', 'Member')])
    
    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.role})"
    
    def save(self, *args, **kwargs):
        if self.role == 'Leader':
            self.user.is_staff = True
            self.user.save()
        else:
            self.user.is_staff = False
            self.user.save()
        super().save(*args, **kwargs)


class ProjectFile(models.Model):
    project = models.ForeignKey(Project, related_name='files', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='pdf')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.project.name})"
    

