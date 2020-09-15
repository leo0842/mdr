from django.db import models

from user.models import User, UserManager

class LecturePost(models.Model):

    title = models.CharField(max_length=200, null=False,blank=False)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lpost')

    objects = UserManager()

    class Meta:
        db_table = "lpost"