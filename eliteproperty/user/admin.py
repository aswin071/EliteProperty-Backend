from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile



class ProfileAdmin(UserAdmin):
    list_display = ('id','profile_photo', 'about', 'date_of_birth', 'state', 'country')
    list_display_links = ('id',)
    ordering = ('id','profile_photo')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(UserProfile, ProfileAdmin)