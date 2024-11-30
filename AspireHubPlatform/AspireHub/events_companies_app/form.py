from django import forms
from .models import Company, Employee, Event

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields ="__all__"

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields ="__all__"

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields ="__all__"