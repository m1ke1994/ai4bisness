from django.urls import path

from apps.subscriptions.views import SubscriptionsAPIView

urlpatterns = [
    path("subscriptions/", SubscriptionsAPIView.as_view(), name="subscriptions"),
]
