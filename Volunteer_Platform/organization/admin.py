from django.contrib import admin
from .models import Organization, Opportunity
from django.utils.html import format_html

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'location')

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'opportunity_type', 'image_preview')
    list_filter = ('category', 'opportunity_type')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return "No Image Available"
    image_preview.short_description = "Image Preview"
