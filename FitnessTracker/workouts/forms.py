from django import forms
from .models import Workout, Set


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['exercise', 'note']
        
# class SetForm(forms.ModelForm):
#     class Meta:
#         model = Set
#         fields = ['weight', 'repetition']
  