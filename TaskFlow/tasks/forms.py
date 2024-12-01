from django import forms
from .models import Task , Comment

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'assigned_to', 'project']
        from django import forms
        widgets = {
            'due_date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',  # Optional, for Bootstrap styling
                'placeholder': 'Select a date'
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
