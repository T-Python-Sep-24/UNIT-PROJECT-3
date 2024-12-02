from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Artist(models.Model):
    PRICE_RANGE_CHOICES = [
            ("$", "Low"),
            ("$$", "Medium"),
            ("$$$", "High"),
            ("$$$$", "Luxury"),
        ]
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255 ,default='Artist')
    about = models.TextField()
    logo = models.ImageField(upload_to="images/",default="static/images/default.png")
    insta_url = models.URLField()
    email = models.EmailField()
    price_range = models.CharField(
        max_length=4,
        choices=PRICE_RANGE_CHOICES,
        default="$$",
        help_text="Price range of the artist's services",
    )
    def __str__(self):
        return self.name

class Photo(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="photos")

    image = models.ImageField(upload_to="images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)



class Review(models.Model):
    class Rate(models.IntegerChoices):
        STAR1 = 1, "One Star"
        STAR2 = 2, "Two Stars"
        STAR3 = 3, "Three Stars"
        STAR4 = 4, "Four Stars"
        STAR5 = 5, "Five Stars"

    artist = models.ForeignKey(Artist,models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.SmallIntegerField(choices=Rate.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    
        