from rest_framework import serializers

from apps.core.models import HeaderMenuLink, SiteHeader


class HeaderMenuLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderMenuLink
        fields = ("title", "href")


class SiteHeaderSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    menu_items = serializers.SerializerMethodField()

    class Meta:
        model = SiteHeader
        fields = ("brand_name", "logo", "logo_link", "menu_items")

    def get_logo(self, obj):
        if not obj.logo:
            return None
        return obj.logo.url

    def get_menu_items(self, obj):
        menu_items = obj.menu_items.filter(is_active=True).order_by("sort_order", "id")
        return HeaderMenuLinkSerializer(menu_items, many=True).data
