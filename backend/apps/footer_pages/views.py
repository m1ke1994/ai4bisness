from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.footer_pages.models import FooterPage
from apps.footer_pages.serializers import FooterPageSerializer


@method_decorator(cache_page(3600), name="dispatch")
class FooterPageListAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        pages = FooterPage.objects.filter(is_published=True).order_by("key", "id")
        serializer = FooterPageSerializer(pages, many=True)
        return Response(serializer.data)


@method_decorator(cache_page(3600), name="dispatch")
class FooterPageDetailAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, slug, *args, **kwargs):
        page = get_object_or_404(FooterPage, slug=slug, is_published=True)
        serializer = FooterPageSerializer(page)
        return Response(serializer.data)
