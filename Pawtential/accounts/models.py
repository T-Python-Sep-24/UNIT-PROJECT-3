from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class IndividualUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='individual_user') 
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    birth_date = models.DateField(null=True,blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/',blank=True , null=True , default='images/default_profile_pic.jpg' )
    phone_number = models.CharField(max_length=15,blank=True,null=True)
    bio = models.TextField(blank=True,null=True)

    USERNAME_FIELD = 'username'  
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
    
class Shelter(models.Model):
        
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shelter')  
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255) 
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True,null=True)
    license_number = models.CharField(max_length=50, unique=True)

    USERNAME_FIELD = 'username'  
    def __str__(self):
        return super().__str__()