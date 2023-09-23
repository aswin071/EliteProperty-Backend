from django.urls import path
from . import views
# from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (TokenRefreshView)
   
    


urlpatterns = [
    # path('api/token/',MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.LoginView.as_view(), name='signin'),
    path('verify-otp/', views.Verify_otpView.as_view(), name='verify_otp'),
    # path("",views.getRoutes)    
]