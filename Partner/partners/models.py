from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    room_name = models.CharField(max_length=200)
    insession = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class Partner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="partners")
    partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="partnered_users")
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.partner.username}"
    class Meta:
        unique_together = ('user', 'partner')  # Prevent duplicate partnerships


class Request(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_requests")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_requests")
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted')], default='pending')
    scheduled_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Request from {self.sender.username} to {self.receiver.username} - {self.status}"



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    readstate=models.BooleanField(default=True)
    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} on {self.created_at}"
