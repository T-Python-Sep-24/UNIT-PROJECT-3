from django.contrib import admin
from .models import Pet

# Register your models here.


class PetAdmin(admin.ModelAdmin):
    list_display = ['name','health_status','adoption_status','user','created_at']
    search_fields=['name','species','location']
    list_filter=['adoption_status']


admin.site.register(Pet, PetAdmin)