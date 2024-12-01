from django import forms
from .models import Task , Comment

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'assigned_to', 'project']
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
