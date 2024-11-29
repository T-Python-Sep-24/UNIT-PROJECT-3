from django.db import models

class Artist(models.Model):
    fullName = models.CharField(max_length=1024, default='Anonymous')
    about = models.TextField()
    birthDate = models.DateField()
    exhibit = models.CharField(max_length=1024)
    photo = models.ImageField(upload_to="images/atrists/", default="images/default.jpg")

    def __str__(self) -> str:
        return f"{self.fullName}"
