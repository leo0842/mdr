from django.db import models
from user.models import User, UserManager
from community.cposting.models import CommunityPost

class CommunityComment(models.Model):
    posts = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='ccomments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ccomments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='creply', null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    class Meta:
        db_table = 'ccomment'
        
