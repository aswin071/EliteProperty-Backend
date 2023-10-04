from rest_framework import serializers
from .models import AdminPayment
from property.serializers import PropertyProfileSerializer

class AdminPaymentSerializer(serializers.ModelSerializer):
    property =PropertyProfileSerializer()
    class Meta:
        model = AdminPayment
        fields = ('id', 'vendor', 'property', 'amount', 'date')

class AdminPaymentviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AdminPayment
        fields = '__all__'





