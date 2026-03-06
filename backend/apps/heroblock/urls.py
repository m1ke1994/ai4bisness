from django.urls import path

from apps.heroblock.views import HeroAPIView

urlpatterns = [
    path("hero/", HeroAPIView.as_view(), name="hero"),
]
