from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to='images/' , default="images/default.png")
    date_added = models.DateField(auto_now_add=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    specialization = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images/' , default="images/default.webp")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')  
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/' , default="images/default.jpeg")  
    specialty = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)  
    linkedin_link = models.URLField(max_length=200, blank=True, null=True)  

    def __str__(self):
        return f"{self.name} - {self.specialty} at {self.company.name}"  