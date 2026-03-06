from django.urls import path

from apps.core.views import HeaderAPIView, HealthCheckAPIView

urlpatterns = [
    path("health/", HealthCheckAPIView.as_view(), name="health-check"),
    path("header/", HeaderAPIView.as_view(), name="header"),
]
