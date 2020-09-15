from rest_framework import serializers
from user.models import User
from lecture.lposting.models import LecturePost
from lecture.lcomment.models import LectureComment

class LectureCommentSerializer(serializers.ModelSerializer):
    lreply = serializers.SerializerMethodField()

    class Meta:
        model = LectureComment
        fields = ('id', 'parent', 'body', 'created_at','updated_at','lreply')

    def get_lreply(self, instance):
        serializer = self.__class__(instance.lreply, many=True)
        serializer.bind('', self)
        return serializer.data
        