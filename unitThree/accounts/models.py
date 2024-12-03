from django.db import models
from django.contrib.auth.models import User
from cards.models import Folder

# Create your models here.

class Profile(models.Model):
    USER_TYPES = (
        ('parent', 'Parent'),
        ('child', 'Child'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='parent')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    about = models.TextField(blank=True)
    parent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    
    def __str__(self):
        return self.user.username