from django import forms
from .models import Group, GroupExpense, GroupGoal, GroupInvitation


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class GroupExpenseForm(forms.ModelForm):
    class Meta:
        model = GroupExpense
        fields = ['category', 'amount']



class GroupGoalForm(forms.ModelForm):
    class Meta:
        model = GroupGoal
        fields = ['name', 'target_amount', 'deadline']





class JoinGroupForm(forms.Form):
    unique_code = forms.CharField(
        label="Group Code",
        max_length=8,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Group Code'})
    )

class GroupContributionForm(forms.Form):
    contribution_type = forms.ChoiceField(choices=[('goal', 'Goal'), ('expense', 'Expense')])
    amount = forms.DecimalField(decimal_places=2, max_digits=10)








class GroupInvitationForm(forms.ModelForm):
    class Meta:
        model = GroupInvitation
        fields = ['email']

