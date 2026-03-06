from rest_framework import serializers

from apps.contacts.models import ContactChannel, ContactsSection


class ContactChannelSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = ContactChannel
        fields = ("name", "icon", "href")

    def get_icon(self, obj):
        if not obj.icon:
            return None
        return obj.icon.url


class ContactsSectionSerializer(serializers.ModelSerializer):
    meta = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = ContactsSection
        fields = (
            "title",
            "subtitle",
            "description",
            "meta",
            "media",
            "channels_title",
            "channels_subtitle",
            "items",
        )

    def get_meta(self, obj):
        return {"headingLine3": obj.heading_line_3}

    def get_media(self, obj):
        return {
            "sectionBackground": obj.section_background.url if obj.section_background else None,
            "cardBackground": obj.card_background.url if obj.card_background else None,
        }

    def get_items(self, obj):
        items = obj.items.filter(is_active=True).order_by("sort_order", "id")
        return ContactChannelSerializer(items, many=True).data
