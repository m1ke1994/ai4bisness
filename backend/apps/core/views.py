from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
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


@method_decorator(cache_page(300), name="dispatch")
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
