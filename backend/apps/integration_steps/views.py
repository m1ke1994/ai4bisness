from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.integration_steps.models import IntegrationStepsSection
from apps.integration_steps.serializers import IntegrationStepsSectionSerializer


@method_decorator(cache_page(300), name="dispatch")
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
                        "titleLines": [],
                        "media": {
                            "background": None,
                            "image": None,
                        },
                    },
                }
            )

        serializer = IntegrationStepsSectionSerializer(steps_section)
        return Response(serializer.data)
