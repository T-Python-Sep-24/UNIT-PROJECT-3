from django.db import models
from django.contrib.auth.models import User
from funds_app.models import Fund
# Create your models here.


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='images/avatars', default='images/avatars/profileAvatar.jpg')

    def __str__(self):
        return f"{self.user.username} Profile"


class UserMessage(models.Model):

    sender = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='sender')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    subject = models.CharField(max_length=1024, blank=True)
    content = models.TextField(default=None)
    is_viewed = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"from: {self.sender} at {self.sent_at}"


class Bookmark(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
