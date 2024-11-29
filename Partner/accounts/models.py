from django.db import models
from django.contrib.auth.models import User
from blogs.models import Blog
from main.models import Language
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    about = models.TextField(blank=True)
    avatar=models.ImageField(upload_to="images/avatars/",default="images/avatars/avatar.webp")
    native_language=models.ForeignKey(Language,related_name="native_language",on_delete=models.CASCADE)
    target_language=models.ForeignKey(Language,related_name="goal_language",on_delete=models.CASCADE)
    class GenderChoices(models.TextChoices):
        MALE='M',"Male"
        FEMALE='F',"Female"
    
    gender=models.CharField(max_length=24, choices=GenderChoices.choices, default=GenderChoices.MALE)
    def __str__(self) -> str:
        return f"Profile {self.user.username}"
    

class Bookmark(models.Model):

    user=models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        pass
