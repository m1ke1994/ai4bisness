from rest_framework.response import Response
from rest_framework.views import APIView

from apps.effectiveness.models import EffectivenessSection
from apps.effectiveness.serializers import EffectivenessSectionSerializer


class EffectivenessAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        section = EffectivenessSection.objects.first()
        if not section:
            return Response(
                {
                    "training": {
                        "title": "",
                        "right_pill": "",
                        "right_title": "",
                        "items": [],
                    },
                    "summary": {
                        "subtitle": "",
                        "title": "",
                        "desktop_stage_label": "",
                        "desktop_ai_label": "",
                        "desktop_human_label": "",
                        "mobile_ai_label": "",
                        "mobile_human_label": "",
                        "stage_description_label": "",
                        "desktop_footer": "",
                        "items": [],
                    },
                }
            )

        serializer = EffectivenessSectionSerializer(section)
        return Response(serializer.data)
