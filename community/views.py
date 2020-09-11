from django.shortcuts import render

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from community.posting.serializers import CommunityPostSerializer
from community.posting.models import CommunityPost

# Create your views here.

class CommunityPostPublishView(CreateAPIView):
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save(author=self.request.user)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': "True",
            "status code": status_code,
            "message": "Post published!",
            "json": serializer.data
        }
        return Response(response, status=status_code)