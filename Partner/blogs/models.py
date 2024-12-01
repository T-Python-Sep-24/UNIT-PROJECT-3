from django.db import models
from main.models import Language
from django.contrib.auth.models import User
# Create your models here.
def get_admin_user():
    """Fetch the admin user and return their ID."""
    admin_user = User.objects.filter(is_superuser=True).first()
    if admin_user:
        return admin_user.id  # Return the ID of the admin user
    return None 

class Blog(models.Model):
    title= models.CharField(max_length=1064)
    image=models.ImageField(upload_to="images/",default="default.jpg")
    content = models.TextField()
    url_video=models.URLField(blank=True,null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True) 
    written_by=models.ForeignKey(User,on_delete=models.PROTECT,default=get_admin_user)
    def __str__(self):
        return self.title
    

class Comment(models.Model):
    blog=models.ForeignKey(Blog, on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment= models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.id} on {self.blog.title}"    