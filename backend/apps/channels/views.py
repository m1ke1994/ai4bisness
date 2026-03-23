from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.channels.models import ChannelsSection
from apps.channels.serializers import ChannelsSectionSerializer


@method_decorator(cache_page(300), name="dispatch")
class ChannelsAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        section = ChannelsSection.objects.first()
        if not section:
            return Response(
                {
                    "title": "",
                    "subtitle": "",
                    "description": "",
                    "meta": {"itemAriaLabelPrefix": ""},
                    "media": {
                        "background": None,
                        "image": None,
                        "secondaryImage": None,
                    },
                    "items": [],
                }
            )

        serializer = ChannelsSectionSerializer(section)
        return Response(serializer.data)
