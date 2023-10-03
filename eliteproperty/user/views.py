from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Account
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
# Create your views here.


#UserProfile
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            print(request.data)
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
                

            return Response({'message': ' Request sent successfully.You can see your Updates on your Profile'}, status=status.HTTP_200_OK)
        except Exception as e:
         
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


#PropertyDetailsInProfile

class PropertyDetailsProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        
        request_details = Interest.objects.filter(user=request.user)
        serializer = InterestPropertySerializer(request_details, many=True)
            
        return Response(serializer.data, status=status.HTTP_200_OK)

# class GetUserPropertyBookings(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user  # Get the current authenticated user
#         user_property_bookings = PropertyBooking.objects.filter(user=user)
#         serializer = PropertyBookingSerializer(user_property_bookings, many=True)
        
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class GetUserPropertyBookings(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user  # Get the current authenticated user
        
#         # Fetch property bookings related to the particular user
#         user_property_bookings = PropertyBooking.objects.filter(user=user)
#         booking_serializer = PropertyBookingSerializer(user_property_bookings, many=True)
        
       
#         property_id = 21  # Replace with the desired property_id
#         property_details = Property.objects.get(pk=property_id)
#         property_serializer = SinglePropertySerializer(property_details)
        
#         response_data = {
#             "property_booking": booking_serializer.data,
#             "property_details": property_serializer.data
#         }
        
#         return Response(response_data, status=status.HTTP_200_OK)

# class GetUserPropertyBookings(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         user = request.user  # Get the current authenticated user
        
#         try:
#             # Fetch property bookings related to the particular user
#             user_property_bookings = PropertyBooking.objects.filter(user=user)
            
#             # Serialize the property booking details
#             property_booking_serializer = PropertyBookingSerializer(user_property_bookings, many=True)
            
#             # Extract property_ids from user_property_bookings
#             property_ids = [booking.property_id for booking in user_property_bookings]
            
#             # Fetch property details for the property_ids
#             property_details = Property.objects.filter(id__in=property_ids)
            
#             # Serialize the property details
#             property_serializer = SinglePropertySerializer(property_details, many=True)
            
#             response_data = {
#                 "property_booking": property_booking_serializer.data,
#                 "property_details": property_serializer.data
#             }
            
#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
# class GetUserPropertyBookings(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user  # Get the current authenticated user

#         # Fetch all property booking details related to the particular user
#         user_property_bookings = PropertyBooking.objects.filter(user=user)
#         property_booking_serializer = PropertyBookingSerializer(user_property_bookings, many=True)

#         return Response(property_booking_serializer.data, status=status.HTTP_200_OK)


# class PropertyPaymentDetails(APIView):

#     permission_classes = [IsAuthenticated]
    
#     def get(self, request, interest_id):

#         try:
            
#             interest = Interest.objects.get(pk=interest_id)
#             print(interest)
#             property = interest.property

            
#             serializer = SingleRequestPropertySerializer(interest)

#             response_data = {
#                 'message': 'Property found',
#                 'propertyData': serializer.data,
#             }

#             return Response(response_data, status=status.HTTP_200_OK)

#         except Interest.DoesNotExist:
#             return Response({'message': 'Interest not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Property.DoesNotExist:
#             return Response({'message': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)

class PropertyPaymentDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, property_id):
        try:
            # Retrieve interest data for the given property_id
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
            
            print(f"Property retrieved: {property}")

            # Check if there are any existing bookings for the same property and user
            existing_bookings = RentBooking.objects.filter(
                property=property,
                user=request.user,
            )
            
            print(f"Existing bookings: {existing_bookings}")

            if existing_bookings.exists():
                # Bookings exist for the same property and user
                serializer = RentForBookingSerializer(existing_bookings, many=True)
                response_data = {
                    'message': 'Property found',
                    'propertyData': serializer.data,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                # No bookings found for the same property and user
                return Response({'message': 'Rent details not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle any exceptions that occur during the request processing
            print(f"Error: {str(e)}")
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
