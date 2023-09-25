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
from property.serializers import AllPropertySerializer,PropertyProfileSerializer,SingleRequestPropertySerializer
from buyproperty.models import Interest
from buyproperty.serializers import interestModelSerializer,InterestPropertySerializer,RentForBookingSerializer,RentBookingSerializer
from buyproperty.models import RentBooking
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

class PropertyPaymentDetails(APIView):

    permission_classes = [IsAuthenticated]
    
    def get(self, request, interest_id):

        try:
            
            interest = Interest.objects.get(pk=interest_id)
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


class GetUserProperties(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        properties = RentBooking.objects.filter(user=request.user)   
        serializer = RentForBookingSerializer(properties, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



class GeneratePDFView(APIView):
    def get(self, request, property_id):
        # Get property details based on property_id
        property = get_object_or_404(Interest, id=property_id)

        # Serialize property data using your serializer
        property_data = InterestPropertySerializer(property).data

        # Render HTML template with serialized property data
        html_template = render_to_string('property_details.html', {'property': property_data})

        # Generate PDF from HTML using pdfkit
        pdf = pdfkit.from_string(html_template, False)

        # Create a response with PDF content
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="property_details.pdf"'

        return response