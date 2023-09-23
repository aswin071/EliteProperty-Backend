from django.urls import path
from .views import (InitiatePaymentView,SuccessPaymentView,RentBookingView,SuccessRentPaymentView,InitiateRentPaymentView)

urlpatterns = [
    path('initiate-payment/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('success-payment/', SuccessPaymentView.as_view(), name='success-payment'),
    path('rent-booking/', RentBookingView.as_view(), name='rent-booking'),
    path('initiate-rent-payment/', InitiateRentPaymentView.as_view(), name='initiate-payment'),
    path('success-rent-payment/', SuccessRentPaymentView.as_view(), name='success-payment'),
   
]

