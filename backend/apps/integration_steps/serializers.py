from rest_framework import serializers

from apps.integration_steps.models import IntegrationStepItem, IntegrationStepsSection


class IntegrationStepItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = IntegrationStepItem
        fields = ("day", "title", "description", "image")

    def get_image(self, obj):
        if not obj.image:
            return None
        return obj.image.url


class IntegrationStepsSectionSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    cta = serializers.SerializerMethodField()

    class Meta:
        model = IntegrationStepsSection
        fields = ("title", "subtitle", "items", "cta")

    def get_items(self, obj):
        items = obj.items.filter(is_active=True).order_by("sort_order", "id")
        return IntegrationStepItemSerializer(items, many=True).data

    def get_cta(self, obj):
        return {
            "titleLines": [obj.cta_title_line_1, obj.cta_title_line_2],
            "media": {
                "background": obj.cta_background.url if obj.cta_background else None,
                "image": obj.cta_image.url if obj.cta_image else None,
            },
        }
