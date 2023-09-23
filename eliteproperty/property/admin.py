from django.contrib import admin
from .models import Property

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'property_type', 'vendor','address')
    list_display_links = ('id', 'title')
    ordering = ('id', 'title')
    search_fields = ('title', 'description', 'location')  # Add fields you want to search by
    
    # Customize the fieldsets as needed
    fieldsets = (
        ('Property Details', {
            'fields': ('title', 'description','address', 'price', 'property_type', 'location', 'num_bedrooms', 'num_bathrooms', 'property_size','image1','image2','image3','status')
        }),
        ('Vendor Information', {
            'fields': ('vendor',),
        }),
    )

admin.site.register(Property, PropertyAdmin)
