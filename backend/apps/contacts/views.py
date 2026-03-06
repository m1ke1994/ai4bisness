from rest_framework.response import Response
from rest_framework.views import APIView

from apps.contacts.models import ContactsSection
from apps.contacts.serializers import ContactsSectionSerializer


class ContactsAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        contacts_section = ContactsSection.objects.first()
        if not contacts_section:
            return Response(
                {
                    "title": "",
                    "subtitle": "",
                    "description": "",
                    "meta": {"headingLine3": ""},
                    "media": {"sectionBackground": None, "cardBackground": None},
                    "channels_title": "",
                    "channels_subtitle": "",
                    "items": [],
                }
            )

        serializer = ContactsSectionSerializer(contacts_section)
        return Response(serializer.data)
