from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.footer.models import SiteFooter
from apps.footer.serializers import SiteFooterSerializer


@method_decorator(cache_page(300), name="dispatch")
class FooterAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        footer = SiteFooter.objects.first()
        if not footer:
            return Response(
                {
                    "brand_name": "",
                    "logo": None,
                    "logo_link": "",
                    "links": [],
                }
            )

        serializer = SiteFooterSerializer(footer)
        return Response(serializer.data)
