from django.db import models
from artists.models import Artist
from django.contrib.auth.models import User

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

class Comment(models.Model):
    piece = models.ForeignKey(ArtPiece, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} on {self.piece.name}"