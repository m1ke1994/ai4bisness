from rest_framework import serializers

from apps.heroblock.models import HeroBlock, HeroStatItem


class HeroStatItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroStatItem
        fields = ("value", "text")


class HeroBlockSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = HeroBlock
        fields = ("title", "subtitle", "description", "image", "stats_disclaimer", "items")

    def get_image(self, obj):
        if not obj.image:
            return None
        return obj.image.url

    def get_items(self, obj):
        items = obj.items.filter(is_active=True).order_by("sort_order", "id")
        return HeroStatItemSerializer(items, many=True).data
