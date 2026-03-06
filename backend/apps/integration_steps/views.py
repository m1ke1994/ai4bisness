from rest_framework.response import Response
from rest_framework.views import APIView

from apps.integration_steps.models import IntegrationStepsSection
from apps.integration_steps.serializers import IntegrationStepsSectionSerializer


class IntegrationStepsAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        steps_section = IntegrationStepsSection.objects.first()
        if not steps_section:
            return Response(
                {
                    "title": "",
                    "subtitle": "",
                    "items": [],
                    "cta": {
                        "titleLines": ["", ""],
                        "media": {"background": None, "image": None},
                    },
                }
            )

        serializer = IntegrationStepsSectionSerializer(steps_section)
        return Response(serializer.data)
