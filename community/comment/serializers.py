from rest_framework import serializers
from user.models import User
from community.posting.models import CommunityPost
from community.comment.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'parent', 'body', 'created_at','updated_at','reply')

    def get_reply(self, instance):
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind('', self)
        return serializer.data
        