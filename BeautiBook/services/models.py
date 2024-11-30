from django.db import models
from providers.models import Artist
# Create your models here.
class Product(models.Model):
    category_options = [('Jeddah', 'Jeddah'),('Riyadh', 'Riyadh'),('Dammam', 'Dammam'),('Abha', 'Abha')]
    name = models.CharField(max_length=100) 
    about= models.ImageField(upload_to='images/')  
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    city = models.CharField(max_length=255,choices=category_options,default='Jeddah')
    artist = models.ForeignKey(Artist,on_delete=models.CASCADE ,default=8)
    def __str__(self) -> str:
      return self.name
