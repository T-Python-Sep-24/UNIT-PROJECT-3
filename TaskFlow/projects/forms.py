from django import forms
from .models import Project
from Users.models import Roll

class ProjectForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=Roll.objects.filter(name="Team Member"),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'members']
