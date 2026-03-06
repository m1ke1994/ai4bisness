from django.urls import path

from apps.channels.views import ChannelsAPIView

urlpatterns = [
    path("channels/", ChannelsAPIView.as_view(), name="channels"),
]
