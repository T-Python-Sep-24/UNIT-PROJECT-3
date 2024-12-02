from django.contrib import admin
from .models import IndividualUser, Shelter
# Register your models here.

class IndividualUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'phone_number', 'birth_date', 'profile_picture')
    search_fields = ['user__username', 'email', 'first_name', 'last_name']
    list_filter = ['birth_date']


class ShelterAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone_number', 'address', 'license_number', 'profile_picture')
    search_fields = ['user__username', 'name', 'phone_number', 'address']
    list_filter = ['address']

admin.site.register(IndividualUser, IndividualUserAdmin)
admin.site.register(Shelter, ShelterAdmin)
