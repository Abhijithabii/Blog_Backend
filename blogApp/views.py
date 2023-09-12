from django.shortcuts import render
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from .serializers import *
from .sendmail import *
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


User = get_user_model()

class UserRegisterationAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterationSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                send_otp_via_mail(serializer.data['email'])
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)


class VerifyOTP(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            user_otp = request.data.get('otp')
            user = CustomUser.objects.filter(email=email)
            if not user.exists():
                return Response({
                    'status': 400,
                    'message': 'Something Went Wrong',
                    'data': 'invalid email',
                })

            if not user[0].otp == user_otp:
                print('------otp error')
                return Response({
                    'status': 400,
                    'message': 'Something Went Wrong',
                    'data': 'wrong otp',
                })

            user = user.first()
            user.is_verified = True
            user.otp = ''
            user.save()
            return Response({
                'status': 200,
                'message': 'Account Verified',
                'data': {},
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'message': 'Internal Server Error',
                'data': str(e),
            })
        


