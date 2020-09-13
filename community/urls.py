from django.conf.urls import url
from django.urls import path
from community.views import CommunityPostPublishView, CommentView

urlpatterns = [
    path('posts/', CommunityPostPublishView.as_view()),
    path('posts/<int:cpost_id>/comment', CommentView.as_view()),
]