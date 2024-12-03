from django.db import models
from directors.models import Director
import json
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    poster=models.ImageField(upload_to="images/movies_posters/")
    genre = models.ManyToManyField(Genre)
    director = models.ForeignKey(Director, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.title



