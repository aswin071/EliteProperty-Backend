from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserType

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('id','email', 'first_name', 'last_name', 'phone_number','user_type', 'created_date', 'updated_date', 'is_active')
    list_display_links = ('email', 'first_name')
    readonly_fields = ('created_date', 'updated_date')
    ordering = ('-updated_date',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Account, AccountAdmin)
admin.site.register(UserType)
