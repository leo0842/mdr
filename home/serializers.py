from rest_framework import serializers
from lecture.lposting.models import LecturePost

class HomeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = LecturePost
        fields = ('__all__')
