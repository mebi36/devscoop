from rest_framework import generics
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from news.serializers import NewsItemCreationSerializer, NewsItemSerializer
from news.models import NewsItem, ItemTypeChoices


class NewsItemPagination(PageNumberPagination):
    """Pagination class for serializers."""
    page_size = 25


class NewsItemApiListCreateView(generics.ListCreateAPIView):
    """API view to enable addition of news items locally."""

    queryset = NewsItem.objects.all().order_by('id')
    pagination_class = NewsItemPagination
    def get_serializer_class(self):
        if self.request.method == "POST":
            return NewsItemCreationSerializer
        return NewsItemSerializer

    def create(self, request, *args, **kwargs):
        """Validate local newsitem creation."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ensure only stories, poll and jobs are being added here
        if serializer.validated_data["type"] in [
            ItemTypeChoices.POLL_OPTION,
            ItemTypeChoices.COMMENT,
        ]:
            raise serializers.ValidationError(
                {
                    "type": "Can only create top item (story, poll, job) posts here."
                }
            )

        # ensure item does not exist
        title = serializer.validated_data["title"]
        if (
            title not in (None, "")
            and NewsItem.objects.filter(title__iexact=title).exists()
        ):
            raise serializers.ValidationError(
                {"titlte": "News item with same title already exists"}
            )

        self.perform_create(serializer)
        return Response(serializer.data)


class NewsItemObjectApiUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """View for modifying locally generated news items.

    Will only find news items generated locally."""

    queryset = NewsItem.objects.filter(from_hn=False)
    serializer_class = NewsItemSerializer


class NewsItemObjectApiDetailView(generics.RetrieveAPIView):
    """View for only displaying news items."""

    queryset = NewsItem.objects.all()
    serializer_class = NewsItemSerializer
