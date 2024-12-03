from django.db import models
from subjects.models import Subject
from django.contrib.auth.models import User

# Create your models here.
class Flashcard(models.Model):
    name = models.CharField(max_length=256)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, null=True)
    photo = models.ImageField(upload_to="images/", default="images/default.jpg")
    pdf = models.FileField(upload_to="pdfs/", default="pdfs/default.pdf")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True, null=True)
    flashcard_json = models.JSONField(null=True, blank=True)
    test_json = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class Review(models.Model):
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} on {self.game.title}"