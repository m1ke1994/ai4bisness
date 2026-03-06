from rest_framework.response import Response
from rest_framework.views import APIView

from apps.system_integrations.models import SystemIntegrationsSection
from apps.system_integrations.serializers import SystemIntegrationsSectionSerializer


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
