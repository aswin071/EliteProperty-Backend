from rest_framework import serializers
from accounts.serializers import UserViewSerializer
from .models import Property
from accounts.models import Account
from vendor.serializers import VendorSerializer,VendorProfileListSerializer,VendorProfileSerializer
from vendor.models import VendorProfile
from user.models import UserProfile
from buyproperty.models import Interest

class AllPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number']

class VendorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = '__all__'

class SinglePropertySerializer(serializers.ModelSerializer):
    vendor = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = '__all__'

    def get_vendor(self, obj):
        try:
            vendor_profile = VendorProfile.objects.get(vendor=obj.vendor)
            vendor_profile_serializer = VendorProfileSerializer(vendor_profile)
            vendor_serializer = AccountSerializer(obj.vendor)
            return {
                'vendor_profile': vendor_profile_serializer.data,
                'vendor_details': vendor_serializer.data
            }
        except VendorProfile.DoesNotExist:
            return None

class SingleRequestPropertySerializer(serializers.ModelSerializer):
    property = SinglePropertySerializer()  

    class Meta:
        model = Interest
        fields = '__all__'
     


class PropertyProfileSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer() 
    
    class Meta:
        model = Property
        fields = '__all__'  #



class RequestedPropertyUserSerializer(serializers.ModelSerializer):
    property_details = AllPropertySerializer(source='property', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ('user', 'property_details')





