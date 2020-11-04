from django.shortcuts import render, redirect

from rest_framework import status
from rest_framework.generics import (
    CreateAPIView, 
    RetrieveAPIView, 
    GenericAPIView, 
    ListAPIView, 
    ListCreateAPIView, 
    RetrieveUpdateAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

import jwt

from datetime import datetime, timedelta
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserSerializer, 
    UserProfileSerializer,
    PasswordChangeSerializer,
    KakaoSerializer,
    EmailVerificationSerializer,
)
from .models import User
from mdr.settings import SECRET_KEY, SOCIALACCOUNT_PROVIDERS
from django.http import HttpResponse
# Create your views here.
import requests

#from rest_auth.registration.views import SocialLoginView

from allauth.socialaccount.providers.kakao import views as kakao_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from django.core.mail.message import EmailMessage
class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def email_sender(self, body, to_email):
        title = "email verification!"
        email = EmailMessage(title, body, to=[to_email])
        email.send()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_email = User.objects.get(email=serializer.data['email'])
        url = "http://localhost:8000/verify/" + user_email.id.__str__()
        self.email_sender(body=url, to_email=serializer.data['email'])
        status_code = status.HTTP_201_CREATED
        response = {
            'success': "True",
            'status code': status_code,
            'message': "User registered successfully",
            'nickname': serializer.data["nickname"],
        }
        return Response(response, status=status_code)


class UserLoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            "success": "True",
            "status_code": status.HTTP_200_OK,
            "message": "User Logged in successfully",
            "token": serializer.data['token'],
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)

class EmailVerificationView(RetrieveAPIView):
    
    queryset = User.objects.all()
    lookup_url_kwarg = 'id'
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        verified_user = User.objects.get(email=instance)
        verified_user.is_active = True
        verified_user.save()
        print(User.objects.get(email=instance).__dict__)
        return redirect("http://localhost:8000/user")

class UserView(ListAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class KakaoException(Exception):
    pass
class kakaoCallbackView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = KakaoSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        params = serializer.data['code']
        try:
            app_rest_api_key = SOCIALACCOUNT_PROVIDERS['kakao']['APP']['client_id']
            parameter = {
                "grant_type": 'authorization_code',
                "client_id": app_rest_api_key,
                "code": params
            }
            token_request = requests.post("https://kauth.kakao.com/oauth/token", data = parameter)
            token_response_json = token_request.json()
            error = token_response_json.get("error", None)
            
            if error == "None":
                raise KakaoException()
                
            access_token = token_response_json.get("access_token")

            header = "Bearer " + access_token
            profile_request = requests.post(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": header}
            )
            profile_json = profile_request.json()

            kakao_id = profile_json.get("id")
            kakao_email = str(kakao_id) + "@kakao.com"
            try:
                user = User.objects.get(email=kakao_email)
                user_id = user.id.__str__()
                payload = {
                    'user_id': user_id,
                    'username': user.email,
                    'exp': datetime.utcnow() + timedelta(seconds=30),
                    'email': user.email,
                    'nickname': user.nickname,
                }

                token = jwt.encode(payload, SECRET_KEY,algorithm='HS256').decode("UTF-8")

                response = {
                    "success": "True",
                    "status_code": status.HTTP_200_OK,
                    "message": "User Logged in successfully with Kakao",
                    "token": token,
                }
                status_code = status.HTTP_200_OK
                return Response(response, status=status_code)
            except User.DoesNotExist:
                User.objects.create(
                    email=kakao_email,
                    password="",
                    nickname="HI"
                )
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            
        except:
            return HttpResponse(status=status.HTTP_402_PAYMENT_REQUIRED)

class UserProfileView(RetrieveUpdateAPIView):

    queryset = User.objects.all()
    lookup_url_kwarg = 'id'
    serializer_class = UserProfileSerializer
    permission_classes = (AllowAny,)

class PasswordChangeView(UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = (AllowAny,)

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        print(type(self.object))

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("Old_PW")):
                return Response({"old_password": ["Wrong_password"]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("New_PW"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
