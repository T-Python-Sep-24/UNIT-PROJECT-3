from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'sender', 'receiver', 'timestamp', 'read']
    list_filter = ['read', 'timestamp']
    search_fields = ['subject', 'sender__username', 'receiver__username']
