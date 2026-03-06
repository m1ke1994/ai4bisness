from rest_framework import serializers

from apps.system_integrations.models import SystemIntegrationItem, SystemIntegrationsSection


class SystemIntegrationItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = SystemIntegrationItem
        fields = ("title", "description", "image")

    def get_image(self, obj):
        if not obj.image:
            return None
        return obj.image.url


class SystemIntegrationsSectionSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = SystemIntegrationsSection
        fields = ("title", "items")

    def get_items(self, obj):
        items = obj.items.filter(is_active=True).order_by("sort_order", "id")
        return SystemIntegrationItemSerializer(items, many=True).data
