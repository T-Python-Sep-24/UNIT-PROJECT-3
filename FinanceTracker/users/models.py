from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

# Create your models here.




class User(AbstractUser):
    is_shared_user = models.BooleanField(default=False)
    notified_reset = models.BooleanField(default=False)




