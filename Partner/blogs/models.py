from django.db import models
from main.models import Language
# Create your models here.

class Blog(models.Model):
    title= models.CharField(max_length=1064)
    image=models.ImageField(upload_to="images/",default="default.jpg")
    content = models.TextField()
    url_video=models.URLField(blank=True,null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True) 
    def __str__(self):
        return self.title