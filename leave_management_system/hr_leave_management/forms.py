from django import forms
from django.contrib.auth.models import User
from employee_leave.models import LeaveRequest

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']



class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'leave_type', 'reason', 'document', 'manager_reason' , 'hr']

    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    reason = forms.CharField(widget=forms.Textarea, required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.initial.get('leave_type'):
            self.initial['leave_type'] = 'sick'

        if 'leave_type' in self.data:
            if self.data.get('leave_type') == 'other':
                self.fields['reason'].required = True
            else:
                self.fields['reason'].required = False
        elif self.instance and self.instance.leave_type == 'other':
            self.fields['reason'].required = True
