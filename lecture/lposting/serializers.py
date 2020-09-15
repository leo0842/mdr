from rest_framework import serializers
from lecture.lposting.models import LecturePost

class LecturePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = LecturePost
        fields = ('title','content')

class LecturePostDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LecturePost
        fields = ('__all__')