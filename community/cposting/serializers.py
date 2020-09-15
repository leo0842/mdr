from rest_framework import serializers

from community.cposting.models import CommunityPost
class CommunityPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommunityPost
        fields = ('title','content')
        
class CommunityPostDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommunityPost
        fields = ('title','content','id','author')
