from rest_framework import serializers
from accounts.models import Account
from accounts.serializers import UserViewSerializer
from .models import VendorProfile



class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'is_verified', 'is_active']

class VendorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=VendorProfile
        exclude = ('vendor',)
        

class VendorProfileListSerializer(serializers.ModelSerializer):
    vendor=VendorSerializer()

    class Meta:
        model=VendorProfile
        fields = '__all__'


