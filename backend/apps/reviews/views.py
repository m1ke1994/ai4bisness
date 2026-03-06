from rest_framework.response import Response
from rest_framework.views import APIView

from apps.reviews.models import ReviewsSection
from apps.reviews.serializers import ReviewsSectionSerializer


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
