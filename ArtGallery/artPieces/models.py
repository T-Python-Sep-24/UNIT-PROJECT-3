from django.db import models
from artists.models import Artist

class ArtPiece(models.Model):
    name = models.CharField(max_length=1024)
    description = models.TextField()
    photo = models.ImageField(upload_to="images/pieces/", default="images/default.jpg")
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT, null=True)
    price = models.IntegerField()
    isSold = models.BooleanField(default=False)
    currentLocation = models.CharField(max_length=1024)
    addedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.name} by {self.artist.fullName}'
