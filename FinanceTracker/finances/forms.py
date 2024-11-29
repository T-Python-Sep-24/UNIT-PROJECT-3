from django import forms
from .models import Expense, Budget
from users.models import User


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'note']


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'monthly_limit']


class SalaryForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['salary']
