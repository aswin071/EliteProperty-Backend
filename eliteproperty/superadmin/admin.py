from django.contrib import admin
from .models import AdminPayment 

class AdminPaymentAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'property', 'amount', 'date')  
    list_filter = ('vendor', 'property', 'date')  
    search_fields = ('vendor__name', 'property__name')  


admin.site.register(AdminPayment, AdminPaymentAdmin)
