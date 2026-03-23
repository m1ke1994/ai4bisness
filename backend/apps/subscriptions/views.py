from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.subscriptions.models import SubscriptionsSection
from apps.subscriptions.serializers import SubscriptionsSectionSerializer


@method_decorator(cache_page(300), name="dispatch")
class SubscriptionsAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        section = SubscriptionsSection.objects.first()
        if not section:
            return Response(
                {
                    "title": "",
                    "subtitle_prefix": "",
                    "subtitle_highlight": "",
                    "badge_primary": "",
                    "badge_secondary": "",
                    "description": "",
                    "left_label": "",
                    "right_label": "",
                    "paid_title": "",
                    "paid_description": "",
                    "note_description": "",
                    "items": [],
                }
            )

        serializer = SubscriptionsSectionSerializer(section)
        return Response(serializer.data)
