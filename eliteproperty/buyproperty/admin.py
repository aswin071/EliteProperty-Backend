from django.contrib import admin
from .models import RentBooking, Interest, Order,PropertyBooking

# Define the admin class for the Booking model
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'property', 'check_in_date', 'check_out_date', 'payment_status')
    list_display_links = ('id', 'user')
    list_filter = ('payment_status',)
    search_fields = ('user__username', 'property__title')
    date_hierarchy = 'check_in_date'
    
admin.site.register(RentBooking, BookingAdmin)

# Define the admin class for the Interest model
class InterestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'property', 'is_interested', 'initial_deposit', 'property_status')
    list_display_links = ('id', 'user')
    list_filter = ('is_interested', 'property_status')  
    search_fields = ('user__username', 'property__title')
    
admin.site.register(Interest, InterestAdmin)


class PropertyBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'status', 'is_paid', 'booking_date')
    list_filter = ('status', 'is_paid', 'booking_date')
    search_fields = ('user__username', 'property__title')

admin.site.register(PropertyBooking, PropertyBookingAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_property', 'deposit_amount', 'is_paid', 'order_date')
    list_filter = ('is_paid', 'order_date')
    search_fields = ('order_property',)

admin.site.register(Order, OrderAdmin)