from rest_framework import serializers
from .models import *


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name', 'contact_no',
                  'location', 'is_customer', 'is_business', 'is_verified']


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


