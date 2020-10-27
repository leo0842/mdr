from django.shortcuts import render

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

from community.cposting.serializers import CommunityPostSerializer, CommunityPostDetailSerializer
from community.cposting.models import CommunityPost
from community.ccomment.serializers import CommunityCommentSerializer
from community.ccomment.models import CommunityComment
from user.models import User

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

class CommunityPostDetailView(RetrieveUpdateDestroyAPIView):

    queryset = CommunityPost.objects.all()
    lookup_url_kwarg = 'id' 
    serializer_class = CommunityPostDetailSerializer
    permission_classes = (AllowAny,)

class CommunityCommentView(ListCreateAPIView):
    queryset = CommunityComment.objects.all()
    serializer_class = CommunityCommentSerializer
    permission_classes = (AllowAny,)
    lookup_url_kwarg = 'cpost_id'

    def post(self, request, cpost_id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        cpost = CommunityPost.objects.get(id=cpost_id)
        serializer.save(user=self.request.user, posts=cpost)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': "True",
            "status code": status_code,
            "message": "Post published!"
        }
        return Response(response, status=status_code)

class CommunityReplyView(CommunityCommentView):
    lookup_url_kwarg = ('cpost_id','comment_id')

    def post(self, request, cpost_id, comment_id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        cpost = CommunityPost.objects.get(id=cpost_id)
        comment = CommunityComment.objects.get(id=comment_id)
        serializer.save(user=self.request.user, posts=cpost, parent=comment)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': "True",
            "status code": status_code,
            "message": "Post published!"
        }
        return Response(response, status=status_code)
