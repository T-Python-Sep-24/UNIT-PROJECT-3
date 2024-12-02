from django.db import models
from django.contrib.auth.models import User
from Users.models import Roll

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    manager = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name="managed_projects", null=True, blank=True
)
    members = models.ManyToManyField(
        Roll,
        related_name="projects",
        limit_choices_to={'name': 'Team Member'}
    )

    def __str__(self):
        return self.name

