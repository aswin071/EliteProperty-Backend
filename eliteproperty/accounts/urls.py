from django.urls import path
from . import views
from rest_framework_simplejwt.views import (TokenRefreshView)
   
    


urlpatterns = [
    
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.LoginView.as_view(), name='signin'),
    path('verify-otp/', views.Verify_otpView.as_view(), name='verify_otp'),
      
]