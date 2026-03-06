from rest_framework import serializers

from apps.pricing.models import PricingFeature, PricingPlan, PricingSection


class PricingFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingFeature
        fields = ("text",)


class PricingPlanSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()

    class Meta:
        model = PricingPlan
        fields = (
            "title",
            "subtitle",
            "accent_badge",
            "inherit_line",
            "channels",
            "cta_label",
            "cta_link",
            "is_featured",
            "is_dark_card",
            "features",
        )

    def get_features(self, obj):
        features = obj.features.filter(is_active=True).order_by("sort_order", "id")
        return PricingFeatureSerializer(features, many=True).data


class PricingSectionSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = PricingSection
        fields = ("title", "subtitle", "channels_label", "items")

    def get_items(self, obj):
        items = obj.items.filter(is_active=True).order_by("sort_order", "id")
        return PricingPlanSerializer(items, many=True).data
