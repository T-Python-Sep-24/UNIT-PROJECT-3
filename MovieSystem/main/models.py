from django.db import models
from django.contrib.auth.models import User
from movies.models import Screening

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    booked_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Ticket {self.id} for {self.screening.movie.title} by {self.user.username}"
