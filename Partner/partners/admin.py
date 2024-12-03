from django.contrib import admin
from .models import Request,Partner,RoomMember
# Register your models here.
admin.site.register(Request)
admin.site.register(Partner)

admin.site.register(RoomMember)