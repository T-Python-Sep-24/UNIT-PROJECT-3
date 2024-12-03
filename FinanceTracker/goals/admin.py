
from django.contrib import admin
from .models import Goal

# Register your models here.



@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'target_amount', 'current_amount', 'deadline')
    list_filter = ('deadline',)
