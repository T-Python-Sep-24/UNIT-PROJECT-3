from django.db import models
from directors.models import Director
from actors.models import Actor
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # ticket price
    genre = models.ManyToManyField(Genre)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    actors = models.ManyToManyField(Actor)
    
    def __str__(self):
        return self.title

class Screening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.CharField(max_length=200)
    showtime = models.DateTimeField()
    available_seats = models.IntegerField()
    booked_seats = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.movie.title} at {self.showtime}"

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    booked_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Ticket {self.id} for {self.screening.movie.title} by {self.user.username}"

