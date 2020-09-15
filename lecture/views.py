from django.shortcuts import render

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

from lecture.lposting.serializers import LecturePostSerializer, LecturePostDetailSerializer
from lecture.lposting.models import LecturePost
from lecture.lcomment.serializers import LectureCommentSerializer
from lecture.lcomment.models import LectureComment

# Create your views here.

class LecturePostPublishView(ListCreateAPIView):
    queryset = LecturePost.objects.all()
    serializer_class = LecturePostSerializer
    permission_classes = (AllowAny,)

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

class LecturePostDetailView(RetrieveUpdateDestroyAPIView):

    queryset = LecturePost.objects.all()
    lookup_url_kwarg = 'id' 
    serializer_class = LecturePostDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

class LectureCommentView(ListCreateAPIView):
    queryset = LectureComment.objects.all()
    serializer_class = LectureCommentSerializer
    permission_classes = (AllowAny,)
    lookup_url_kwarg = 'lpost_id'

    def post(self, request, lpost_id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        lpost = LecturePost.objects.get(id=lpost_id)
        serializer.save(user=self.request.user, posts=lpost)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': "True",
            "status code": status_code,
            "message": "Post published!"
        }
        return Response(response, status=status_code)

class LectureReplyView(LectureCommentView):
    lookup_url_kwarg = ('lpost_id','comment_id')

    def post(self, request, lpost_id, comment_id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        lpost = LecturePost.objects.get(id=lpost_id)
        comment = LectureComment.objects.get(id=comment_id)
        serializer.save(user=self.request.user, posts=lpost, parent=comment)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': "True",
            "status code": status_code,
            "message": "Post published!"
        }
        return Response(response, status=status_code)

