from rest_framework.response import Response
from rest_framework.views import APIView

from apps.pricing.models import PricingSection
from apps.pricing.serializers import PricingSectionSerializer


class PricingAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        pricing_section = PricingSection.objects.first()
        if not pricing_section:
            return Response(
                {
                    "title": "",
                    "subtitle": "",
                    "channels_label": "",
                    "items": [],
                }
            )

        serializer = PricingSectionSerializer(pricing_section)
        return Response(serializer.data)
