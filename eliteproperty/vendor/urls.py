from django.urls import path
from .views import (VendorProfileView,VendorProfileListView,VendorHomeView,
                        PropertyInquiriesView,UpdatePropertyStatusView,
                        VendorPropertyBookingListView,
                        UserRentBookingVendorSide,
                        UpdateRentPaymentStatusView,
                        UpdateSalePaymentStatusView,
                        AuthenticatedVendorProfile,
                        SaletNetAmount,RentNetAmount,
                        VendorDashBoard)

urlpatterns = [
    path('vendor-createprofile/', VendorProfileView.as_view(), name='create-vendor-profile'),
    path('vendor-createprofile/<int:id>/',VendorProfileView.as_view(), name='update-vendor-profile'),
     path('vendor-profile/', AuthenticatedVendorProfile.as_view(), name='vendor-profile'),
    path("vendor-profiles/",VendorProfileListView .as_view(), name="vednor-profile-list"),
    path("vendor-home-view/", VendorHomeView.as_view(), name="vendor-home"),
    path("property-inquiries/<int:property_id>/",PropertyInquiriesView.as_view(), name="vendor-requested-property"),
    path("manage-property-status/<int:property_id>/",PropertyInquiriesView.as_view(), name="vendor-requested-property"),
    path('update-status/<int:property_id>/', UpdatePropertyStatusView.as_view(), name='update_property_status'),
    path('sale/property-bookings/', VendorPropertyBookingListView.as_view(), name='vendor-sale-property-bookings'),
    path('rent/property-bookings/', UserRentBookingVendorSide.as_view(), name='vendor-property-bookings'),
    path('update-payment-status/<int:booking_id>/', UpdateRentPaymentStatusView.as_view(), name='update-payment-status'),
    path('update-sale/payment-status/<int:booking_id>/', UpdateSalePaymentStatusView.as_view(), name='update-payment-status'),
    path('sale/netamount/', SaletNetAmount.as_view(), name='sale/netamount'),
    path('rent/netamount/', RentNetAmount.as_view(), name='rent/netamount'),
    path('dashboard/', VendorDashBoard.as_view(), name='dashboard'),


]