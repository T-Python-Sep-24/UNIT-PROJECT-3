from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import City, Flight

admin.site.register(City)
admin.site.register(Flight)
