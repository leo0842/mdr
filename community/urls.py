from django.conf.urls import url
from django.urls import path
from community.views import CommunityPostPublishView, CommentView, ReplyView

urlpatterns = [
    path('posts/', CommunityPostPublishView.as_view()),
    path('posts/<int:cpost_id>/comment/', CommentView.as_view()),
    path('posts/<int:cpost_id>/comment/<int:comment_id>/', ReplyView.as_view()),
]