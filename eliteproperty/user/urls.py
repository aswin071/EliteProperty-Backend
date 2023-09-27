from django.urls import path
from .views import (UserProfileView, UserProfileListView,PropertyListView,AuthenticatedUserProfile,
                        BookingRequestView,GetUserPropertyBookings,PropertyPaymentDetails,CheckoutForRentProperty,GetUserBookings,
                        GeneratePDFView,PropertyDetailsProfileView)

urlpatterns = [
    path('user-createprofile/', UserProfileView.as_view(), name='create-user-profile'),
    path('user-createprofile/<int:id>/', UserProfileView.as_view(), name='update-user-profile'),
    path("user/profile/", AuthenticatedUserProfile.as_view(), name="user-profile-home"),
    path('user-profiles/', UserProfileListView.as_view(), name='user-profile-list-admin'),
    path("properties/", PropertyListView.as_view(), name="propeties"),
    path("book-property/", BookingRequestView.as_view(), name="book-property"),
    path("requested-details/", PropertyDetailsProfileView.as_view(), name="requested-details"),
    path('book/property/<int:property_id>/', PropertyPaymentDetails.as_view(), name='property-payment-details'),
    path('rent/book/property/<int:property_id>/', CheckoutForRentProperty.as_view(), name='property-payment-details'),
    path('user-properties/', GetUserBookings.as_view(), name='user-properties'),
    path('generate_pdf/<int:property_id>/',GeneratePDFView.as_view(), name='generate_pdf'),

]