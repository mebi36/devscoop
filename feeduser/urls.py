from django.urls import path

from feeduser.views import CreateFeedUserView, FeedUserDetailView

app_name = "feeduser"


urlpatterns = [
    path("new/", CreateFeedUserView.as_view(), name="new"),
    path("<int:pk>/", FeedUserDetailView.as_view(), name="detail"),
]
