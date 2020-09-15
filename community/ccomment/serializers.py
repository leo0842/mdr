from rest_framework import serializers
from user.models import User
from community.cposting.models import CommunityPost
from community.ccomment.models import CommunityComment

class CommunityCommentSerializer(serializers.ModelSerializer):
    creply = serializers.SerializerMethodField()

    class Meta:
        model = CommunityComment
        fields = ('id', 'parent', 'body', 'created_at','updated_at','creply')

    def get_creply(self, instance):
        serializer = self.__class__(instance.creply, many=True)
        serializer.bind('', self)
        return serializer.data
        