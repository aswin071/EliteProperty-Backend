from django.shortcuts import render
from django.http  import JsonResponse
from rest_framework.response import Response
from  rest_framework.decorators import api_view

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.shortcuts import render
from .models import Account, UserType
from rest_framework import generics
from .serializers import SignUpSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.views import LoginView
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from vendor.models import VendorProfile
from user.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from .token import create_jwt_pair_tokens
import datetime
from .otp import send_otp
# Create your views here.

class SignUpView(APIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            user_type = data.get('user_type')
            email = data.get('email')

            user = serializer.save()

            if user_type == 'Vendor':
                user = Account.objects.get(email = email)
                user_type = UserType.objects.get(user_type_name = 'Vendor')
                user.user_type = user_type
                user.save()
                VendorProfile.objects.create(vendor = user)
                phone_number = data.get('phone_number')
                email = data.get('email')
                username = data.get('username')
                send_otp(username, email)

            elif user_type == 'User':
                user = Account.objects.get(email = email)
                user_type = UserType.objects.get(user_type_name = 'User')
                user.user_type = user_type
                user.save()
                UserProfile.objects.create(user = user)
                phone_number = data.get('phone_number')
                email = data.get('email')
                username = data.get('username')
                send_otp(username, email)

            response = {
                'message': 'User Created Successfully',
                'otp': True
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        else:
            
            error_message = "Error occurred. Please check your inputs"
            if Account.objects.filter(email=data.get('email')).exists():
                error_message = "Email is already taken"
            if Account.objects.filter(phone_number=data.get('phone_number')).exists():
                error_message = "Phone number already taken"
            return Response(data=error_message, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request:Request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_verified == True:
                tokens = create_jwt_pair_tokens(user)
                refresh_token = RefreshToken(tokens['refresh'])

                response = {
                    "message": "Login Successful",
                    "access_token": tokens['access'],
                    "refresh_token": tokens['refresh'],
                    "token_expiry": refresh_token['exp'],
                    "is_login": True,
                    "user": {
                        "user_id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "username": user.username,
                        "phone_number": user.phone_number,
                        "email": user.email,
                        "user_type": user.user_type.user_type_name,
                        "is_active": user.is_active,
                        "is_profile": user.is_profile
                    }
                }
                return Response(data=response, status=status.HTTP_200_OK)

            
            else:
                response = {
                    "message" : "user is not verified"
                }
                return Response(data=response, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        else:
            return Response(data={"message" : "Invalid email or password !"}, status=status.HTTP_400_BAD_REQUEST)


class Verify_otpView(APIView):
    def post(self, request: Request):
        data = request.data
        check_otp = data.get('otp')
        email = data.get('email')

        try:
            user = Account.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({"Failed": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        stored_otp = user.otp

        if stored_otp == check_otp:
            user.is_verified = True
            user.otp = ""  
            user.save()

            return Response(
                data={'Success': 'User is verified', 'is_verified': True},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"Failed": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
            )

