from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import VendorProfile

class ProfileAdmin(UserAdmin):
    list_display = ('id','profile_photo', 'brokerage_fee', 'specialization','city', 'state', 'country', 'year_of_experience', 'age', 'is_registered')
    list_display_links = ('id',)
    ordering = ('id','profile_photo')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(VendorProfile, ProfileAdmin)