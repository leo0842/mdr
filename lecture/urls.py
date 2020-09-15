from django.conf.urls import url
from django.urls import path, include
from lecture.views import LecturePostDetailView, LecturePostPublishView, LectureCommentView, LectureReplyView

urlpatterns = [
    path('posts/', LecturePostPublishView.as_view()),
    path('posts/<int:id>/', LecturePostDetailView.as_view()),
    path('posts/<int:lpost_id>/comment/', LectureCommentView.as_view()),
    path('posts/<int:lpost_id>/comment/<int:comment_id>/', LectureReplyView.as_view()),
]