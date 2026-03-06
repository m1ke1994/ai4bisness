from rest_framework import serializers

from apps.reviews.models import Review, ReviewsSection


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "id",
            "company",
            "person",
            "preview_text",
            "preview_bullets",
            "details_text",
            "results",
        )


class ReviewsSectionSerializer(serializers.ModelSerializer):
    meta = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = ReviewsSection
        fields = ("title", "subtitle", "meta", "items")

    def get_meta(self, obj):
        return {
            "modal_results_title": obj.modal_results_title,
            "actions": {
                "readMore": obj.read_more_label,
                "prevPageAria": obj.prev_page_aria,
                "nextPageAria": obj.next_page_aria,
                "paginationAria": obj.pagination_aria,
                "paginationGoTo": obj.pagination_go_to_label,
                "closeModalAria": obj.close_modal_aria,
            },
        }

    def get_items(self, obj):
        items = obj.items.filter(is_active=True).order_by("sort_order", "id")
        return ReviewSerializer(items, many=True).data
