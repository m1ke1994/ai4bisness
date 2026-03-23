from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.system_integrations.models import SystemIntegrationsSection
from apps.system_integrations.serializers import SystemIntegrationsSectionSerializer


@method_decorator(cache_page(300), name="dispatch")
class SystemIntegrationsAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        section = SystemIntegrationsSection.objects.first()
        if not section:
            return Response(
                {
                    "title": "",
                    "items": [],
                }
            )

        serializer = SystemIntegrationsSectionSerializer(section)
        return Response(serializer.data)
