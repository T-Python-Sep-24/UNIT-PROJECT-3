from django.contrib import admin
from .models import Opportunity

class OpportunityAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'location', 'date_posted']  # Removed 'start_date' and 'end_date'
    list_filter = ['organization', 'date_posted']  # Removed 'start_date'

admin.site.register(Opportunity, OpportunityAdmin)
