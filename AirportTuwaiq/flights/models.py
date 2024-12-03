from django.db import models

# Create your models here.
from django.db import models

class City(models.Model):
    # Simple model to store unique city names
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Flight(models.Model):
    # Unique identifier for the flight
    flight_number = models.CharField(max_length=20, unique=True)

    # Links to the City model for origin and destination cities
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='departures')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='arrivals')

    # Flight timing information
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    # Flight pricing and seat availability
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.flight_number}: {self.from_city} to {self.to_city} at {self.departure_time}"
    