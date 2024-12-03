from celery import shared_task
from datetime import date
from .models import Expense

@shared_task
def reset_monthly_expenses():
    current_month = date.today().month
    current_year = date.today().year
    expenses_to_reset = Expense.objects.filter(date__month=current_month, date__year=current_year)
    count = expenses_to_reset.count()
    expenses_to_reset.delete()
    return f"Reset {count} expenses for {current_month}/{current_year}"
