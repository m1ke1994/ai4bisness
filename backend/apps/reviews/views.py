from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.reviews.models import ReviewsSection
from apps.reviews.serializers import ReviewsSectionSerializer


@method_decorator(cache_page(300), name="dispatch")
class ReviewsAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        reviews_section = ReviewsSection.objects.first()
        if not reviews_section:
            return Response(
                {
                    "title": "",
                    "subtitle": "",
                    "meta": {
                        "modal_results_title": "",
                        "actions": {
                            "readMore": "",
                            "prevPageAria": "",
                            "nextPageAria": "",
                            "paginationAria": "",
                            "paginationGoTo": "",
                            "closeModalAria": "",
                        },
                    },
                    "items": [],
                }
            )

        serializer = ReviewsSectionSerializer(reviews_section)
        return Response(serializer.data)
