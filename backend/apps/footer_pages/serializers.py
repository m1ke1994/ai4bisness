from rest_framework import serializers

from apps.footer_pages.models import FooterPage


class FooterPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterPage
        fields = ("key", "slug", "title", "content")

