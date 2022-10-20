from rest_framework import serializers

from .models import TopItem, Comment, PollOption


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments."""
    class Meta:
        model = Comment
        fields = "__all__"


class PollOptionSerializer(serializers.ModelSerializer):
    """Serializer for poll options."""  
    class Meta:
        model = PollOption
        fields = "__all__"
                                     

class TopItemSerializer(serializers.ModelSerializer):
    """Serializer for TopItem model."""
    class Meta:
        model = TopItem
        fields = "__all__"
    
    def get_comments(self, obj):
        return CommentSerializer(queryset=Comment.objects.filter(content_object_id=obj), many=True)

    

class TopItemCreationSerializer(TopItemSerializer):
    """Serializer for adding news item locally."""
    class Meta:
        model = TopItem
        exclude = ('ext_id', 'id', 'from_hn')
    

class PollSerializer(TopItemSerializer):
    """Serializer for Polls."""                                     
    pollopts = PollOptionSerializer(many=True)

