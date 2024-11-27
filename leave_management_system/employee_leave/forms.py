from django import forms
from .models import LeaveRequest

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'leave_type', 'reason', 'document']

    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    reason = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'leave_type' in self.data:
            if self.data.get('leave_type') == 'other':
                self.fields['reason'].required = True
            else:
                self.fields['reason'].required = False
        elif self.instance and self.instance.leave_type == 'other':
            self.fields['reason'].required = True

        if not self.initial.get('leave_type'):
            self.initial['leave_type'] = 'sick'
