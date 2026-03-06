from rest_framework import serializers

from apps.footer.models import FooterLink, SiteFooter


class FooterLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterLink
        fields = ("title", "href")


class SiteFooterSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()

    class Meta:
        model = SiteFooter
        fields = ("brand_name", "logo", "logo_link", "links")

    def get_logo(self, obj):
        if not obj.logo:
            return None
        return obj.logo.url

    def get_links(self, obj):
        links = obj.links.filter(is_active=True).order_by("sort_order", "id")
        return FooterLinkSerializer(links, many=True).data
