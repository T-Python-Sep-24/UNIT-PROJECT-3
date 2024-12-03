from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid
from decimal import Decimal
# Create your models here.


class Group(models.Model):
    SHARED_GOAL = 'shared_goal'


    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_groups'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='group_memberships'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    pending_invitations = models.JSONField(default=list)

    shared_goal_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shared_goal_current = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monthly_expense_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class GroupGoal(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='goal')
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deadline = models.DateField()

    def progress(self):
        if self.target_amount == 0:
            return 0
        return (self.current_amount / self.target_amount) * 100

    def remaining_amount(self):
        return max(self.target_amount - self.current_amount, 0)

    def per_user_share(self):
        total_members = self.group.members.count()
        return self.remaining_amount() / total_members if total_members > 0 else 0

    def __str__(self):
        return f"{self.name} - {self.progress()}%"





class GroupExpense(models.Model):
    CATEGORY_CHOICES = [
        ('rent', 'Rent'),
        ('food', 'Food'),
        ('petrol', 'Petrol'),
        ('groceries', 'Groceries'),
        ('entertainment', 'Entertainment'),
        ('health', 'Health'),
        ('other', 'Other'),
    ]

    group = models.OneToOneField(
        Group, 
        on_delete=models.CASCADE, 
        related_name='expense'
    )  
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other'
    )  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    contributed_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0))  
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='created_expenses'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.group.name} - {self.get_category_display()} - {self.amount}"

    @property
    def remaining_amount(self):
        return max(Decimal(0), self.amount - self.contributed_amount)

    @property
    def is_fully_funded(self):
        return self.remaining_amount == 0








class Contribution(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='contributions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_for_goal = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'user', 'is_for_goal')

    def __str__(self):
        return f"{self.user.username} - {'Goal' if self.is_for_goal else 'Expense'} - {self.amount}"



class GroupMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="memberships")
    monthly_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ("user", "group")

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"




class GroupInvitation(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="invitations")
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at  = models.DateTimeField(auto_now_add=True)

