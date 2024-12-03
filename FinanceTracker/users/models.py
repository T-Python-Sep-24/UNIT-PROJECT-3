from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_shared_user = models.BooleanField(default=False)
    notified_reset = models.BooleanField(default=False)
    savings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    photo = models.ImageField(
        upload_to='profile_photos/',
        default='profile_photos/default.png',  
        blank=True
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  


    def __str__(self):
        return self.username




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    total_contributions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Profile"
