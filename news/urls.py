from django.urls import path

from news.views import LatestNewsItemListView, NewsItemApiListCreateView, NewsItemDetailView

app_name = 'news'
urlpatterns = [
    path("latest", LatestNewsItemListView.as_view(), name="latest"),
    path("detail/<str:pk>", NewsItemDetailView.as_view(), name="detail"),
    
    # api urls
    path("items/", NewsItemApiListCreateView.as_view(), name='items')
]
