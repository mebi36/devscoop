from django.urls import path

from news.views import LatestTopItemListView


urlpatterns = [
    path("latest", LatestTopItemListView.as_view(), name="latest")
]