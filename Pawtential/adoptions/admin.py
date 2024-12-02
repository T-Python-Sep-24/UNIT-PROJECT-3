from django.contrib import admin
from .models import AdoptionRequest


# Register your models here.

class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'pet')
    search_fields = ('user__username', 'pet__name')

admin.site.register(AdoptionRequest, AdoptionRequestAdmin)