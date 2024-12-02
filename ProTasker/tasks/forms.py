
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status', 'due_date', 'project', 'assignee']
    
    
    priority = forms.ChoiceField(choices=Task.priority_choices, required=True)
