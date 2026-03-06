from django.urls import path

from apps.integration_steps.views import IntegrationStepsAPIView

urlpatterns = [
    path("integration-steps/", IntegrationStepsAPIView.as_view(), name="integration-steps"),
]
