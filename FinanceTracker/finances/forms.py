from django import forms
from .models import Expense, Budget, CATEGORY_CHOICES
from users.models import User



class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'note']
        widgets = {
        'date': forms.DateInput(attrs={'type': 'date'}),  
    }
    category = forms.ChoiceField(choices=[(k, v) for k, v in CATEGORY_CHOICES if k != 'goal_contributions'])

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'monthly_limit']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }




class SalaryForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['salary']
