from django.contrib import admin
from .models import Category, Location, Testimonial ,Profile

admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Profile)

from django.contrib import admin
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')
    search_fields = ('user__username', 'content')
