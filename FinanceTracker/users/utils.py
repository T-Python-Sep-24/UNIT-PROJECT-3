from django.core.mail import send_mail
from .models import User
from django.db.models import Sum
from decimal import Decimal


def notify_users():
    users = User.objects.filter(notified_reset=False)
    for user in users:
        send_mail(
            'Monthly Expense Reset',
            'Your expenses have been reset for the month.',
            'admin@yourdomain.com',
            [user.email],
        )
        user.notified_reset = True
        user.save()



def update_user_savings(user, amount):
    """
    Updates the savings of a user by deducting the given amount.
    Returns the updated remaining savings.
    """
    user.savings -= Decimal(amount)
    user.save()
    total_expenses = user.expenses.aggregate(total_spent=Sum('amount'))['total_spent'] or Decimal(0)
    remaining_savings = user.savings - total_expenses
    return remaining_savings


def update_user_savings(user, contribution_amount):
    user.savings -= contribution_amount
    user.save()

    total_expenses = user.expenses.aggregate(total_spent=Sum('amount'))['total_spent'] or Decimal(0)
    return user.savings - total_expenses