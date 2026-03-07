from rest_framework import serializers

from apps.subscriptions.models import SubscriptionItem, SubscriptionsSection


class SubscriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionItem
        fields = ("text",)


class SubscriptionsSectionSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = SubscriptionsSection
        fields = (
            "title",
            "subtitle_prefix",
            "subtitle_highlight",
            "badge_primary",
            "badge_secondary",
            "description",
            "left_label",
            "right_label",
            "paid_title",
            "paid_description",
            "note_description",
            "items",
        )

    def get_items(self, obj):
        items = obj.items.filter(is_active=True).order_by("sort_order", "id")
        return SubscriptionItemSerializer(items, many=True).data
