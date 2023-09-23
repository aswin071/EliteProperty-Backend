from rest_framework import serializers
from .models import Interest,Order,PropertyBooking,RentBooking
from accounts.serializers import UserViewSerializer
from user.serializers import UserProfileListSerializer,UserProfileSerializer,AllPropertySerializer
from property.serializers import AllPropertySerializer,SinglePropertySerializer
from user.models import UserProfile
from property.models import Property


class interestModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interest
        fields = '__all__'

class InterestSerializer(serializers.ModelSerializer):
    user = UserViewSerializer()
    class Meta:
        model = Interest
        fields = '__all__'

class InterestPropertySerializer(serializers.ModelSerializer):

    property=AllPropertySerializer()

    class Meta:
        model = Interest
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class PropertyBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyBooking
        fields = '__all__'


class PropertyTransactionSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()
    property_details = serializers.SerializerMethodField()

    class Meta:
        model = PropertyBooking
        fields = '__all__'

    def get_user_details(self, obj):
        user = obj.user
        return {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            
        }

    def get_property_details(self, obj):
        property = obj.property
        return {
            'property_id': property.id,
            'property_title': property.title,
            'property_description': property.description,
            
        }

class RentBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentBooking
        fields = '__all__'



class RentForBookingSerializer(serializers.ModelSerializer):

    property=SinglePropertySerializer()

    class Meta:
        model = RentBooking
        fields = '__all__'






