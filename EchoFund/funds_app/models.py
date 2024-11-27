from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Fund(models.Model):

    founder = models.ForeignKey(User, on_delete=models.PROTECT, related_name='founder')
    fund_members = models.ManyToManyField(User, related_name='members')
    fund_name = models.CharField(max_length=100)
    about = models.TextField()
    policies = models.TextField()
    monthly_stock = models.SmallIntegerField()
    hold_duration = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
