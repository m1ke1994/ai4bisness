from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import SiteHeader
from apps.core.serializers import SiteHeaderSerializer


class HealthCheckAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "status": "ok",
                "message": "Django backend is running",
            }
        )


class HeaderAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        header = SiteHeader.objects.first()
        if not header:
            return Response(
                {
                    "brand_name": "",
                    "logo": None,
                    "logo_link": "",
                    "menu_items": [],
                }
            )

        serializer = SiteHeaderSerializer(header)
        return Response(serializer.data)
