from django.db import models
from users.models import UserProfile

class Review(models.Model):
    reviewer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='given_reviews')
    reviewee = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_reviews')
    content = models.TextField()
    rating = models.IntegerField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer} for {self.reviewee}"
