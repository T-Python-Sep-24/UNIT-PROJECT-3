from django.db import models
from users.models import User
from django.contrib.auth.models import User
from django.conf import settings
from decimal import Decimal

CATEGORY_CHOICES = [
    ('rent', 'Rent'),
    ('food', 'Food'),
    ('petrol', 'Petrol'),
    ('groceries', 'Groceries'),
    ('entertainment', 'Entertainment'),
    ('health', 'Health'),
    ('other', 'Other'),
    ('goal_contributions', 'Goal Contributions'),
]

class Expense(models.Model):
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"


class Budget(models.Model):
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    monthly_limit = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.monthly_limit}"






