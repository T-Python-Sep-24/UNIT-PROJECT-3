from django.contrib import admin
from .models import Profile, Bookmark, UserMessage
# Register your models here.

admin.site.register(Profile)
admin.site.register(Bookmark)

class msgAdmin(admin.ModelAdmin):
    list_display = 'sender', 'is_viewed'
admin.site.register(UserMessage, msgAdmin)