from django.urls import path

from apps.effectiveness.views import EffectivenessAPIView

urlpatterns = [
    path("effectiveness/", EffectivenessAPIView.as_view(), name="effectiveness"),
]
