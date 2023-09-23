from rest_framework import serializers
from accounts.models import Account
from .models import UserProfile
from accounts.serializers import UserViewSerializer
from property.serializers import AllPropertySerializer


#user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'is_verified', 'is_active']

#Userprofile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        exclude = ('user',)

#UserProfileListing
class UserProfileListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'

class UserPropertySerializer(serializers.ModelSerializer):
    property = AllPropertySerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'profile_photo', 'about', 'date_of_birth', 'state', 'country', 'property')
        
    extra_kwargs = {

        'property': {'write_only': True},  # Allow writing the property field
    }


