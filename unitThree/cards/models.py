from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Folder(models.Model):
    CATEGORY_CHOICES = [
        ('EN', 'English'),
        ('MA', 'Math'),
        ('PR', 'Programming'),
        ('SC', 'Science'),
        ('OT', 'Other'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='folders')
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default='OT')  # Ensure this line exists
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class Flashcard(models.Model):
    question = models.TextField()
    answer = models.TextField()
    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        related_name='flashcards'  
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flashcards', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} on {self.question[:50]}"