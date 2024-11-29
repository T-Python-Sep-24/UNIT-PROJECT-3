from django.db import models
from users.models import UserProfile, Skill  # Ensure correct imports

class Opportunity(models.Model):
    organization = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="opportunities"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    time_commitment = models.CharField(max_length=100)
    posted_date = models.DateTimeField(auto_now_add=True)
    required_skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="opportunities"
    )

    def __str__(self):
        return self.title
