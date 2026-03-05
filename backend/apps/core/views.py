from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import (
    AdvantagesSection,
    AiValueSection,
    ChannelsSection,
    ContactsSection,
    FooterSection,
    HeaderSection,
    HeroLogosSection,
    HeroSection,
    PolicyPage,
    PricingSection,
    ReviewsSection,
    SiteSettings,
    StepsSection,
)
from apps.core.serializers import (
    AdvantagesSectionSerializer,
    AiValueSectionSerializer,
    ChannelsSectionSerializer,
    ContactsSectionSerializer,
    FooterSectionSerializer,
    HeaderSectionSerializer,
    HeroLogosSectionSerializer,
    HeroSectionSerializer,
    PolicyPageSerializer,
    PricingSectionSerializer,
    ReviewsSectionSerializer,
    SiteSettingsSerializer,
    StepsSectionSerializer,
    serialize_site_data,
)


def health_check(request):
    return JsonResponse({"status": "ok"})


class SiteSettingsAPIView(APIView):
    def get(self, request):
        instance = get_object_or_404(SiteSettings)
        serializer = SiteSettingsSerializer(instance, context={"request": request})
        return Response(serializer.data)


class HeaderSectionAPIView(APIView):
    def get(self, request):
        instance = get_object_or_404(HeaderSection)
        serializer = HeaderSectionSerializer(instance, context={"request": request})
        return Response(serializer.data)


class HeroSectionAPIView(APIView):
    def get(self, request):
        instance = get_object_or_404(HeroSection)
        serializer = HeroSectionSerializer(instance, context={"request": request})
        return Response(serializer.data)


class HeroLogosSectionAPIView(APIView):
    def get(self, request):
        instance = get_object_or_404(HeroLogosSection)
        serializer = HeroLogosSectionSerializer(instance, context={"request": request})
        return Response(serializer.data)


class AdvantagesSectionAPIView(APIView):
    def get(self, request):
        instance = get_object_or_404(AdvantagesSection)
        serializer = AdvantagesSectionSerializer(instance, context={"request": request})
        return Response(serializer.data)


class AiValueSectionAPIView(APIView):
    def get(self, request):
        instance = get_object_or_404(AiValueSection)
        serializer = AiValueSectionSerializer(instance, context={"request": request})
        return Response(serializer.data)


class ChannelsSectionAPIView(APIView):
    def get(self, request):
        instance = get_object_or_404(ChannelsSection)
        serializer = ChannelsSectionSerializer(instance, context={"request": request})
        return Response(serializer.data)


class StepsSectionAPIView(APIView):
    def get(self, request):
        instance = get_object_or_404(StepsSection)
        serializer = StepsSectionSerializer(instance, context={"request": request})
        return Response(serializer.data)


class PricingSectionAPIView(APIView):
    def get(self, request):
        instance = get_object_or_404(PricingSection)
        serializer = PricingSectionSerializer(instance, context={"request": request})
        return Response(serializer.data)


class ReviewsSectionAPIView(APIView):
    def get(self, request):
        instance = get_object_or_404(ReviewsSection)
        serializer = ReviewsSectionSerializer(instance, context={"request": request})
        return Response(serializer.data)


class ContactsSectionAPIView(APIView):
    def get(self, request):
        instance = get_object_or_404(ContactsSection)
        serializer = ContactsSectionSerializer(instance, context={"request": request})
        return Response(serializer.data)


class FooterSectionAPIView(APIView):
    def get(self, request):
        instance = get_object_or_404(FooterSection)
        serializer = FooterSectionSerializer(instance, context={"request": request})
        return Response(serializer.data)


PAGE_SLUG_MAP = {
    "privacy": "privacy-policy",
    "offer": "public-offer",
    "terms": "user-agreement",
}


class PolicyPageAPIView(APIView):
    def get(self, request, slug: str):
        mapped_slug = PAGE_SLUG_MAP.get(slug, slug)
        instance = get_object_or_404(PolicyPage, slug=mapped_slug, is_active=True)
        serializer = PolicyPageSerializer(instance, context={"request": request})
        return Response(serializer.data)


class SiteDataAPIView(APIView):
    def get(self, request):
        return Response(serialize_site_data(request))
