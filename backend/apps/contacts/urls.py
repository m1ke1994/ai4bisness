from django.urls import path

from apps.contacts.views import ContactsAPIView

urlpatterns = [
    path("contacts/", ContactsAPIView.as_view(), name="contacts"),
]
