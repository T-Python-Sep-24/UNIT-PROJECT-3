from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to='companies/')
    date_added = models.DateField(auto_now_add=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    specialization = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='events/')
    date = models.DateField()

    def __str__(self):
        return self.title

class Personality(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='personalities')
    name = models.CharField(max_length=200)
    specialty = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)  # New field for description
    linkedin_link = models.URLField(max_length=200, blank=True, null=True)  # New field for LinkedIn link

    def __str__(self):
        return self.name
