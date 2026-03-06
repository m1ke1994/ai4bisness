from rest_framework import serializers

from apps.channels.models import ChannelItem, ChannelsSection


class ChannelItemSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = ChannelItem
        fields = ("name", "href", "icon")

    def get_icon(self, obj):
        return {
            "src": obj.icon.url if obj.icon else None,
            "alt": obj.name,
        }


class ChannelsSectionSerializer(serializers.ModelSerializer):
    meta = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = ChannelsSection
        fields = ("title", "subtitle", "description", "meta", "media", "items")

    def get_meta(self, obj):
        return {"itemAriaLabelPrefix": obj.item_aria_label_prefix}

    def get_media(self, obj):
        return {
            "background": obj.background.url if obj.background else None,
            "image": obj.image.url if obj.image else None,
            "secondaryImage": obj.secondary_image.url if obj.secondary_image else None,
        }

    def get_items(self, obj):
        items = obj.items.filter(is_active=True).order_by("sort_order", "id")
        return ChannelItemSerializer(items, many=True).data
