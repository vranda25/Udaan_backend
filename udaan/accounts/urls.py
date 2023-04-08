from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verifyotp/', VerfiyOTPView.as_view()),
    path('login/', LoginView.as_view()),
]