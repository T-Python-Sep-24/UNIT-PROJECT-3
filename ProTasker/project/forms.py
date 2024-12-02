from django import forms
from .models import Project, TeamMember
from django.forms import modelformset_factory


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'priority', 'manager', 'due_date', 'status']  
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter project description'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'manager': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  
            'status': forms.Select(attrs={'class': 'form-select'}),  
        }



class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['user', 'role']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

    TeamMemberFormSet = modelformset_factory(
        TeamMember,
        fields=('user', 'role'),
        extra=5,  
        can_delete=True,
    )
