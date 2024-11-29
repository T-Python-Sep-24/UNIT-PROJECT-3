from django import forms
from .models import Goal

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'target_amount', 'deadline']  
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),  
        }

class AddMoneyToGoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['current_amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['current_amount'].widget = forms.NumberInput(attrs={'type': 'number', 'min': 0, 'step': '0.01'})