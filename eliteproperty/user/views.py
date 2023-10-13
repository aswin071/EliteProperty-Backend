from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Account
from django.db import IntegrityError
from django.conf import settings
import pdfkit
from django.template.loader import render_to_string
from .models import UserProfile
from .serializers import UserProfileSerializer, UserProfileListSerializer
from property.models import Property
from property.serializers import AllPropertySerializer,PropertyProfileSerializer,SingleRequestPropertySerializer,SinglePropertySerializer
from buyproperty.models import Interest,PropertyBooking
from buyproperty.serializers import interestModelSerializer,InterestPropertySerializer,RentForBookingSerializer,RentBookingSerializer,RentPropertyBookingSerializer,PropertyBookingSerializer,PropertyTransactionSerializer
from buyproperty.models import RentBooking,RentPropertyBooking
from django.shortcuts import get_object_or_404
from .signals import property_interest_signal
from django.core.mail import send_mail
from django.dispatch import receiver

# Create your views here.


#UserProfile
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'message': 'user profile not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=request.user)
            user = Account.objects.get(email = request.user)
            user.is_profile = True
            user.save()
        except UserProfile.DoesNotExist:
            return Response({'message': 'user profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# UserProfileDetails
class AuthenticatedUserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileListSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'message': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

# UserProfileListing
class UserProfileListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profiles = UserProfile.objects.all()
        serializer = UserProfileListSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#UserProperty View

class PropertyListView(APIView):
    def get(self, request, *args, **kwargs):
        properties = Property.objects.filter(is_published=True)
        serializer = PropertyProfileSerializer(properties, many=True)  # Use PropertyProfileSerializer
        return Response(serializer.data, status=status.HTTP_200_OK)

#VendorHomelist
class VendorHomeView(APIView):
    
    def get(self, request, *args, **kwargs):
        profiles=VendorProfile.objects.all()
        serializer = VendorProfileListSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
       

#InterestProperty

class BookingRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        property_id = request.data.get('property_id')

        try:
            interest, created = Interest.objects.get_or_create(user=user, property_id=property_id)

            if created:
                interest.is_interested = True
                interest.save()
                
                

            property_interest_signal.send(sender=Interest, booking=interest)

            
                
            return Response({'message': ' Request sent successfully.You can see your Updates on your Profile'}, status=status.HTTP_200_OK)
        except IntegrityError as e:
            
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

#PropertyDetailsInProfile

class PropertyDetailsProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        
        request_details = Interest.objects.filter(user=request.user)
        serializer = InterestPropertySerializer(request_details, many=True)
            
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserPropertyBookings(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user  
        
        try:
            
            user_property_bookings = PropertyBooking.objects.filter(user=user)
            
            
            property_booking_serializer = PropertyBookingSerializer(user_property_bookings, many=True)
            
           
            property_ids = [booking.property_id for booking in user_property_bookings]
            
           
            property_details = Property.objects.filter(id__in=property_ids)
            
           
            property_serializer = SinglePropertySerializer(property_details, many=True)
            
           
            interest_details = Interest.objects.filter(user=user)
            interest_serializer = InterestPropertySerializer(interest_details, many=True)
            
            response_data = {
                "property_booking": property_booking_serializer.data,
                "property_details": property_serializer.data,
                "interest_details": interest_serializer.data  # Include interest details in the response
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PropertyPaymentDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, property_id):
        try:
            
            interest = Interest.objects.get(property_id=property_id)
            property = interest.property

            serializer = SingleRequestPropertySerializer(interest)

            response_data = {
                'message': 'Property found',
                'propertyData': serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Interest.DoesNotExist:
            return Response({'message': 'Interest not found'}, status=status.HTTP_404_NOT_FOUND)
        except Property.DoesNotExist:
            return Response({'message': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)

  
class CheckoutForRentProperty(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, property_id):
        try:
            # Retrieve the property
            property = get_object_or_404(Property, id=property_id)
            

            existing_bookings = RentBooking.objects.filter(
                property=property,
                user=request.user,
            )
            
            

            if existing_bookings.exists():
                
                serializer = RentForBookingSerializer(existing_bookings, many=True)
                response_data = {
                    'message': 'Property found',
                    'propertyData': serializer.data,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                
                return Response({'message': 'Rent details not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
           
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetUserBookings(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user 
        user_bookings = RentPropertyBooking.objects.filter(user=user)
        booking_serializer = RentPropertyBookingSerializer(user_bookings, many=True)
        
        property_ids = [booking['property'] for booking in booking_serializer.data]
        
        
        properties = Property.objects.filter(id__in=property_ids)
        property_serializer = SinglePropertySerializer(properties, many=True)
        
        
        combined_data = [
            {
                'booking': booking,
                'property': property
            }
            for booking, property in zip(booking_serializer.data, property_serializer.data)
        ]
        
        return Response(combined_data, status=status.HTTP_200_OK)



class UserSaleBookings(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        user_bookings=PropertyBooking.objects.filter(user=user)
        booking_serializer = PropertyBookingSerializer(user_bookings, many=True)

        property_ids = [booking['property'] for booking in booking_serializer.data]
        
        
        properties = Property.objects.filter(id__in=property_ids)
        property_serializer = SinglePropertySerializer(properties, many=True)
        
        
        combined_data = [
            {
                'userbooking': booking,
                'property': property
            }
            for booking, property in zip(booking_serializer.data, property_serializer.data)
        ]
        
        return Response(combined_data, status=status.HTTP_200_OK)


@receiver(property_interest_signal)
def send_vendor_sale_notification(sender, booking, **kwargs):
    
    vendor_redirect = "https://elite-property.vercel.app/vendor/property/inquiries"
    vendor_subject = "New Booking Notification"
    vendor_message = (
        f'Hello, you have a new booking for your property "{booking.property.title}".\n\n'
        f'Please log in to your vendor account to manage this booking and respond to the customer.\n\n'
        f'You can view and manage the booking by clicking on the following link:\n\n'
        f'{vendor_redirect}\n\n'
        f'Best regards,\nYour Real Estate Team'
    )

   
    send_mail(
        vendor_subject,
        vendor_message,
        settings.EMAIL_HOST_USER,
        [booking.property.vendor.email],
        fail_silently=False,
    )


@receiver(property_interest_signal)
def send_vendor_rent_notification(sender, booking, **kwargs):
    
    vendor_redirect = "https://elite-property.vercel.app/vendor/property/inquiries"
    vendor_subject = "New Booking Notification"
    vendor_message = (
        f'Hello, you have a new booking for your property "{booking.property.title}".\n\n'
        f'Please log in to your vendor account to manage this booking and respond to the customer.\n\n'
        f'You can view and manage the booking by clicking on the following link:\n\n'
        f'{vendor_redirect}\n\n'
        f'Best regards,\nYour Real Estate Team'
    )

    
    send_mail(
        vendor_subject,
        vendor_message,
        settings.EMAIL_HOST_USER,
        [booking.property.vendor.email],
        fail_silently=False,
    )
    