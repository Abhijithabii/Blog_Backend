from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print("inside the serializer")
        if not user.is_verified:
            return AuthenticationFailed('User is not verified.')
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['is_active'] = user.is_active
        token['is_superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff
        return token
    


class UserRegisterationSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "password", "is_verified"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    






