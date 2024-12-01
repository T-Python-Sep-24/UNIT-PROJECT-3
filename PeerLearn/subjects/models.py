from django.db import models

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=256)
    logo = models.ImageField(upload_to="images/", default="images/default.jpg")
    about = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
