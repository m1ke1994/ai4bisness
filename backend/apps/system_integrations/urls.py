from django.urls import path

from apps.system_integrations.views import SystemIntegrationsAPIView

urlpatterns = [
    path("system-integrations/", SystemIntegrationsAPIView.as_view(), name="system-integrations"),
]
