from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from .models import User

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

class UserRegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('email', 'password', 'nickname')
        extra_kwargs = {"password": {"write_only":True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        
        return user

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        print("email and password are ", email, password)
        user = authenticate(email=email, password=password)
        print("this user is ", user)
        if user is None:
            raise serializers.ValidationError(
        "A user with this email and password is not found."
        )
        try:
            print("typeofuser", type(user))
            payload = JWT_PAYLOAD_HANDLER(user)
            payload['nickname'] = User.objects.get(email=user).nickname
            print("payload: ",payload)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)

        except User.DoesNotExist:
            raise serializers.ValidationError(
        "User with given email and password does not exists"
        )
        return {
            'email': user.email,
            'token': jwt_token
        }

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('__all__')

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','nickname')

class EmailVerificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('__all__')
class PasswordChangeSerializer(serializers.ModelSerializer):
    Old_PW = serializers.CharField(required=True)
    New_PW = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','Old_PW','New_PW')

class KakaoSerializer(serializers.ModelSerializer):
    client_id = serializers.CharField(required=True)
    code =serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('client_id','code')