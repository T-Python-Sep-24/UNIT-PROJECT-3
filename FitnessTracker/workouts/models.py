from django.db import models
from django.contrib.auth.models import User
from exercises.models import Exercise
from routines.models import Routine

class Workout(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    note = models.TextField(blank=True)
    restTime = models.PositiveIntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.routine.name}-{self.exercise.name}'


class Set(models.Model):
    weight = models.FloatField()
    repetition = models.PositiveIntegerField()
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.workout.routine.name}-{self.workout.exercise.name} set: {self.id}'
     
     
class Check(models.Model):

    set = models.OneToOneField(Set, on_delete=models.CASCADE, related_name='check')
    created_at = models.DateTimeField(auto_now_add=True)