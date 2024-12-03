from django.db import models
from movies.models import Movie
from django.contrib.auth.models import User
import json

# Create your models here.
class Screening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.CharField(max_length=200)
    showtime = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    seats = models.TextField(default=json.dumps({
        "A1": True, "A2": True, "A3": True, "A4": True, "A5": True, "A6": True,
        "B1": True, "B2": True, "B3": True, "B4": True, "B5": True, "B6": True,
        "C1": True, "C2": True, "C3": True, "C4": True, "C5": True, "C6": True,
        "D1": True, "D2": True, "D3": True, "D4": True, "D5": True, "D6": True,
    }))
    def get_seats(self):
        return json.loads(self.seats)
    
    @property
    def available(self):
        seats = self.get_seats()
        return any(value for value in seats.values())
    
    def __str__(self):
        return f"{self.movie.title} at {self.showtime}"

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    seat_numbers = models.JSONField()  
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"Ticket {self.id} for {self.screening.movie.title} by {self.user.username}"
