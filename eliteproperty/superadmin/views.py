from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Account
from rest_framework.parsers import MultiPartParser, FormParser
from vendor.models import VendorProfile
from property.models import Property
from property.serializers import AllPropertySerializer
# Create your views here.

class VendorRegistrationApprovalView(APIView):
    def post(self, request, vendor_id):
        try:
            profile = VendorProfile.objects.get(vendor_id=vendor_id)
            profile.is_registered = True  # Approve registration
            profile.save()
            return Response({'message': 'Registration approved'}, status=status.HTTP_200_OK)
        except VendorProfile.DoesNotExist:
            return Response({'message': 'Vendor profile not found'}, status=status.HTTP_404_NOT_FOUND)

class BlockUnblockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,user_id):
        try:
            instance=Account.objects.get(id=user_id)
            instance.is_active= not instance.is_active
            instance.save()

            return Response({"message": "User status changed"}, status=status.HTTP_200_OK)

        except Account.DoesNotExist:

            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class BlockUnblockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,user_id):
        try:
            instance=Account.objects.get(id=user_id)
            instance.is_active= not instance.is_active
            instance.save()

            return Response({"message": "User status changed"}, status=status.HTTP_200_OK)

        except Account.DoesNotExist:

            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class PublishUnpublishProperty(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch all property data
        properties = Property.objects.all()
        # Serialize the property data using your serializer (PropertySerializer)
        serializer = AllPropertySerializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request,prop_id):
       

        try:
            instance = Property.objects.get(id=prop_id)
            instance.is_published = not instance.is_published
            instance.save()

            return Response({"message":"Property accepted"}, status=status.HTTP_404_NOT_FOUND)

        except Property.DoesNotExist:
            
            return Response({"message": "Property not found"}, status=status.HTTP_404_NOT_FOUND)

