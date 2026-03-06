from rest_framework.response import Response
from rest_framework.views import APIView

from apps.heroblock.models import HeroBlock
from apps.heroblock.serializers import HeroBlockSerializer


class HeroAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        hero_block = HeroBlock.objects.first()
        if not hero_block:
            return Response(
                {
                    "title": "",
                    "subtitle": "",
                    "description": "",
                    "image": None,
                    "stats_disclaimer": "",
                    "items": [],
                }
            )

        serializer = HeroBlockSerializer(hero_block)
        return Response(serializer.data)
