from django.contrib import admin
from .models import Profile, Bookmark, UserMessage
# Register your models here.

admin.site.register(Profile)
admin.site.register(Bookmark)
admin.site.register(UserMessage)