from rest_framework import serializers

from .models import NewsItem, Comment, PollOption


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


class NewsItemSerializer(serializers.ModelSerializer):
    """Serializer for NewsItem model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="news:api-object-modify"
    )
    comments = CommentSerializer(many=True)

    class Meta:
        model = NewsItem
        fields = "__all__"


class NewsItemCreationSerializer(NewsItemSerializer):
    """Serializer for adding news item locally."""

    class Meta:
        model = NewsItem
        exclude = ("ext_id", "id", "from_hn")


class PollSerializer(NewsItemSerializer):
    """Serializer for Polls."""

    pollopts = PollOptionSerializer(many=True)
