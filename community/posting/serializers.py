from rest_framework import serializers

from community.posting.models import CommunityPost
class CommunityPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommunityPost
        fields = ('title','content')
class CommunityPostDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommunityPost
        fields = ('title','content','id','author')
