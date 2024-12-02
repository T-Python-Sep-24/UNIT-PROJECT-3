from django.contrib import admin
from .models import Volunteer, Application

class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'profile_picture']
    filter_horizontal = ['skills']

admin.site.register(Volunteer, VolunteerAdmin)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['volunteer', 'opportunity', 'status', 'date_applied']
    list_filter = ['status', 'date_applied']
    search_fields = ['volunteer__user__username', 'opportunity__title']
