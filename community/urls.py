from django.conf.urls import url
from django.urls import path
from community.views import CommunityPostPublishView

urlpatterns = [
    path('create/', CommunityPostPublishView.as_view()),
]