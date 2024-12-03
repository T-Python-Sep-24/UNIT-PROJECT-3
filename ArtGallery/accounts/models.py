from django.db import models
from django.contrib.auth.models import User
from artPieces.models import ArtPiece

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True)
    pfp = models.ImageField(upload_to="images/usersPfps/", default="images/usersPfps/defaultPfp.jpg")

    def __str__(self) -> str:
        return f'Profile {self.user.username}'

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    piece = models.ForeignKey(ArtPiece, on_delete=models.CASCADE)
    addedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s favorites"