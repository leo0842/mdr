from django.conf.urls import url
from django.urls import path
from community.views import CommunityPostPublishView, CommunityPostDetailView, CommunityCommentView, CommunityReplyView

urlpatterns = [
    path('posts/', CommunityPostPublishView.as_view()),
    path('posts/<int:id>/', CommunityPostDetailView.as_view()),
    path('posts/<int:cpost_id>/comment/', CommunityCommentView.as_view()),
    path('posts/<int:cpost_id>/comment/<int:comment_id>/', CommunityReplyView.as_view()),
]