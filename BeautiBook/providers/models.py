from django.db import models

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255 ,default='Artist')
    about = models.TextField()
    insta_url = models.URLField()
    email = models.EmailField()
    
    def __str__(self):
        return self.name

class Photo(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)