from django.urls import path

from news.views import LatestTopItemListView, TopItemAPIListCreateView


urlpatterns = [
    path("latest", LatestTopItemListView.as_view(), name="latest"),
    
    path("items/", TopItemAPIListCreateView.as_view(), name='items')
]
