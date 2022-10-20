from django.urls import path

from news.views import LatestTopItemListView, TopItemApiListCreateView


urlpatterns = [
    path("latest", LatestTopItemListView.as_view(), name="latest"),
    
    path("items/", TopItemApiListCreateView.as_view(), name='items')
]
