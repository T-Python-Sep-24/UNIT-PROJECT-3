from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Fund(models.Model):

    fund_name = models.CharField(max_length=100)
    about = models.TextField()
    policies = models.TextField()
    monthly_stock = models.SmallIntegerField()
    hold_duration = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):

    class Rates(models.IntegerChoices):

        STAR1 = 1, 'One Star'
        STAR2 = 2, 'Two Stars'
        STAR3 = 3, 'Three Stars'
        STAR4 = 4, 'Four Stars'
        STAR5 = 5, 'Five Stars'

    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(choices=Rates.choices)
    comment = models.TextField()
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} on {self.fund.fund_name}"