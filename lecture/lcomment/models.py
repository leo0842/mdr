from django.db import models
from user.models import User, UserManager
from lecture.lposting.models import LecturePost

class LectureComment(models.Model):
    posts = models.ForeignKey(LecturePost, on_delete=models.CASCADE, related_name='lcomments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lcomments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='lreply', null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    class Meta:
        db_table = 'lcomment'