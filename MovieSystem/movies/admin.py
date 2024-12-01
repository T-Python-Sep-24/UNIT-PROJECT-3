from django.contrib import admin
from .models import Genre , Movie ,Screening ,Ticket
# Register your models here.

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Screening)
admin.site.register(Ticket)
