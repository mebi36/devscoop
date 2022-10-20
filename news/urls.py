from django.urls import path

from news.views import (
    LatestNewsItemListView,
    NewsItemApiListCreateView,
    NewsItemDetailView,
    NewsItemObjectApiUpdateDeleteView,
)

app_name = "news"
urlpatterns = [
    path("latest", LatestNewsItemListView.as_view(), name="latest"),
    path("detail/<str:pk>", NewsItemDetailView.as_view(), name="detail"),
    # api urls
    path("item/all/", NewsItemApiListCreateView.as_view(), name="all-items"),
    path(
        "item/<str:pk>",
        NewsItemObjectApiUpdateDeleteView.as_view(),
        name="api-object-modify",
    ),
]
