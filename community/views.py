from django.shortcuts import render

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

from community.posting.serializers import CommunityPostSerializer, CommunityPostDetailSerializer
from community.posting.models import CommunityPost
from community.comment.serializers import CommentSerializer
from community.comment.models import Comment
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
    permission_classes = (IsAuthenticatedOrReadOnly,)

class CommentView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
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

class ReplyView(CommentView):
    lookup_url_kwarg = ('cpost_id','comment_id')

    def post(self, request, cpost_id, comment_id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        cpost = CommunityPost.objects.get(id=cpost_id)
        comment = Comment.objects.get(id=comment_id)
        serializer.save(user=self.request.user, posts=cpost, parent=comment)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': "True",
            "status code": status_code,
            "message": "Post published!"
        }
        return Response(response, status=status_code)

