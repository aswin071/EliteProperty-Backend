from django.contrib import admin
from .models import AdminPayment 

class AdminPaymentAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'property', 'amount', 'date')  
    list_filter = ('vendor', 'property', 'date')  
    search_fields = ('vendor__name', 'property__name')  

# Register the VendorPayment model with the custom admin class
admin.site.register(AdminPayment, AdminPaymentAdmin)
