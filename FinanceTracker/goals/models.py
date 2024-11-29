from django.db import models
from users.models import User

# Create your models here.




class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    deadline = models.DateField()

    def progress(self):
        if self.target_amount == 0:
            return 0.0
        return (self.current_amount / self.target_amount) * 100

    def __str__(self):
        return f"{self.name} ({self.progress():.2f}%)"
