from django.contrib import admin
from .models import Volunteer, VolunteerApplication

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'skills')
    search_fields = ('user__username', 'skills')

@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'opportunity', 'status', 'applied_at')
    list_filter = ('status',)
    search_fields = ('volunteer__user__username', 'opportunity__title')
