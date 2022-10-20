from rest_framework import serializers

from .models import TopItem, Comment


class TopItemSerializer(serializes.ModelSerializer):
    """Serializer for listing news items and adding news items locally."""
    comments = serializers.SerializerMethodField()
    class Meta:
        model = TopItem
        exclude = ['id', 'ext_id']
        def get_comments(self, obj):
            return CommentSerializer(queryset=Comment.objects.filter(content_object=obj)
                                     
                                     
class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments."""
    class Meta:
        model = Comment
        fields = ["__all__"]
