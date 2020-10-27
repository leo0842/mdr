from django.shortcuts import render

from lecture.lposting.models import LecturePost

from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .serializers import HomeListSerializer
# Create your views here.

class HomeListView(ListAPIView):

    queryset = LecturePost.objects.all().order_by('-published_at')[:3]
    serializer_class = HomeListSerializer
    permission_classes = (AllowAny,)