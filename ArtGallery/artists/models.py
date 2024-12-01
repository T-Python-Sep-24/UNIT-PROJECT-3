from django.db import models

class Artist(models.Model):
    fullName = models.CharField(max_length=1024)
    about = models.TextField()
    birthDate = models.DateField()
    exhibit = models.CharField(max_length=1024)
    photo = models.ImageField(upload_to="images/atrists/", default="images/usersPfps/defaultPfp.jpg")
    addedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.fullName}"
