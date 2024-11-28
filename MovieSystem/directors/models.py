from django.db import models

# Create your models here.
class Director(models.Model):
    name = models.CharField(max_length=200)
    biography = models.TextField()
    
    def __str__(self):
        return self.name