from django.db import models
from django.contrib.auth.models import User

class Routine(models.Model):
    name = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    all_weights = models.PositiveBigIntegerField(default=0, blank=True)
    is_public = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.name