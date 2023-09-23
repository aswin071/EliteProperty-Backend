
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Property
from .serializers import AllPropertySerializer,PropertyProfileSerializer,SinglePropertySerializer
from vendor.models import VendorProfile
from vendor.serializers import VendorProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser

#Create your views here.

class AddPropertyView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, format=None):
        try:
            
            # Retrieve and serialize properties based on your logic
            properties = Property.objects.filter(vendor=request.user)
            serializer = AllPropertySerializer(properties, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'message': 'Failed to retrieve properties', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        try:
           
            property_data = request.data
            property_data['vendor'] = request.user.id

            serializer = AllPropertySerializer(data=property_data)
            if serializer.is_valid():
                serializer.save()
                response_data = {"message": "Property added successfully", "data": serializer.data}
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': 'Failed to add property', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SinglePropertyView(APIView):
    def get(self, request, id):
        try:
            property = Property.objects.get(id=id)
            serializer = SinglePropertySerializer(property)
            response_data = {'message': 'Property found', 'singledata': serializer.data}
            return Response(response_data, status=status.HTTP_200_OK)
        except Property.DoesNotExist:
            return Response({'message': 'Property not Found'}, status=status.HTTP_404_NOT_FOUND)



