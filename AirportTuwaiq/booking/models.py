from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from flights.models import Flight
import uuid


class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]

    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="bookings")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateTimeField(auto_now_add=True)
    seats = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking {self.booking_id} - {self.customer.username} for Flight {self.flight.flight_number}"