import bcrypt

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer
from .models import User

class UserApi(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():

            if User.objects.filter(name=serializer.validated_data["name"]).exists():

                return Response({"message": "EXISTS_NAME"}, status=status.HTTP_400_BAD_REQUEST)

            temp_password = serializer.validated_data["password"] 
            temp_password = bcrypt.hashpw(temp_password.encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")
            serializer.validated_data["password"] = temp_password
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
