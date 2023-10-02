from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from accounts.models import Account
from .models import VendorProfile
from rest_framework.generics import RetrieveAPIView
from .serializers import(VendorProfileSerializer,VendorProfileListSerializer)
from rest_framework.permissions import AllowAny 
from property.serializers import RequestedPropertyUserSerializer,AllPropertySerializer
from user.models import UserProfile
from property.models import Property
from user.serializers import UserProfileListSerializer
from buyproperty.serializers import InterestSerializer,RentPropertyUpdateBookingSerializer
from buyproperty.models import Interest,RentPropertyBooking
from buyproperty.serializers import PropertyBookingSerializer,PropertyTransactionSerializer,RentBookingSerializer,RentPropertyBookingSerializer,RentPropertyHistorySerializer
from buyproperty.models import PropertyBooking
# Create your views here.


class VendorProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        try:
            profile = VendorProfile.objects.get(vendor=request.user)
            serializer = VendorProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except VendorProfile.DoesNotExist:
            return Response({'message': 'Vendor profile not found'}, status=status.HTTP_404_NOT_FOUND)

   
    def put(self, request, *args, **kwargs):
       
        try:
           
            profile, created = VendorProfile.objects.get_or_create(vendor=request.user)
            

           
            user = Account.objects.get(email=request.user)
            user.is_profile = True
            user.save()
          
        except Exception as e:
           
            return Response({'message': 'Failed to create/update vendor profile'}, status=status.HTTP_400_BAD_REQUEST)

        
        serializer = VendorProfileSerializer(profile, data=request.data)
        
    
        if serializer.is_valid():
            
            if 'profile_photo' in request.FILES:
                profile.profile_photo = request.FILES['profile_photo']

            serializer.save()
          
            return Response({'message': 'Created/Updated successfully'}, status=status.HTTP_200_OK)
        else:
           
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorProfileListView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profiles=VendorProfile.objects.all()
        serializer = VendorProfileListSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VendorHomeView(APIView):
    
    def get(self, request, *args, **kwargs):
        profiles=VendorProfile.objects.all()
        serializer = VendorProfileListSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      



class PropertyInquiriesView(APIView):

    permission_classes=[IsAuthenticated]

    def get(self, request, property_id):
        # Filter interests based on the property
        interests = Interest.objects.filter(property_id=property_id)

        # Serialize the interests to include user details
        serializer = InterestSerializer(interests, many=True)

        return Response({'inquiries': serializer.data}, status=status.HTTP_200_OK)


    def post(self, request, property_id):

        try:
          
            vendor = request.user
            interest = Interest.objects.get( property_id=property_id)
            
            property_status = request.data.get('property_status')
            deposit_amount = request.data.get('deposit_amount', None)

            interest.property_status = property_status

            # Only update the deposit amount if property_status is not 'sold'
            if property_status != 'sold':
                interest.initial_deposit = deposit_amount

            interest.save()

            return Response({'message': 'Property status updated successfully.'}, status=status.HTTP_200_OK)

        except Interest.DoesNotExist:
            return Response({'message': 'No interest found for the specified property and vendor.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)






class UpdatePropertyStatusView(APIView):
    permission_classes=[IsAuthenticated]
    def put(self, request, property_id):
        property_instance = get_object_or_404(Property, pk=property_id)

        if request.user == property_instance.vendor:
            new_status = request.data.get('status')

            property_instance.status = new_status
            property_instance.save()

            return Response({'message': 'Property status updated successfully.'})

        return Response({'error': 'You are not authorized to update the property status.'}, status=403)
   


class VendorPropertyBookingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
       
        vendor = self.request.user 
        bookings = PropertyBooking.objects.filter(property__vendor=vendor)
        serializer = PropertyTransactionSerializer(bookings, many=True)
        return Response(serializer.data)

class UserRentBookingVendorSide(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
       
        vendor = self.request.user 
        bookings = RentPropertyBooking.objects.filter(property__vendor=vendor)
        serializer = RentPropertyHistorySerializer(bookings, many=True)
        return Response(serializer.data)



class UpdatePaymentStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, booking_id):
        print('ID:', booking_id)
        property_instance = get_object_or_404(RentPropertyBooking, pk=booking_id)

        new_status = request.data.get('status')
        print(new_status)

        if new_status in dict(RentPropertyBooking.STATUS_CHOICES):
            property_instance.status = new_status
            property_instance.save()
            print('yes')
            return Response({'message': 'Property payment status updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid status choice.'}, status=status.HTTP_400_BAD_REQUEST)

