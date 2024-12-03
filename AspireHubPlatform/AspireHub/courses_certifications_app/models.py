from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    duration = models.CharField(max_length=50)  # E.g., "3 weeks", "6 months"
    prerequisites = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', default='images/default.jpg')

    def __str__(self):
        return self.title


class Certification(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    classification = models.CharField(max_length=100)  # E.g., "Professional", "Basic", "Advanced"
    cost = models.DecimalField(max_digits=10, decimal_places=2)  # Cost of testing
    estimated_study_time = models.CharField(max_length=50)  # E.g., "4 weeks", "60 hours"
    image = models.ImageField(upload_to='images/', default='images/default.jpg')

    def __str__(self):
        return self.name