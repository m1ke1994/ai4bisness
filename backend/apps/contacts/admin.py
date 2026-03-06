from django.contrib import admin

from apps.contacts.models import ContactChannel, ContactsSection


class ContactChannelInline(admin.TabularInline):
    model = ContactChannel
    extra = 1
    fields = ("name", "icon", "href", "sort_order", "is_active")
    ordering = ("sort_order", "id")


@admin.register(ContactsSection)
class ContactsSectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "subtitle",
        "heading_line_3",
        "channels_title",
        "channels_subtitle",
    )
    search_fields = (
        "title",
        "subtitle",
        "heading_line_3",
        "description",
        "channels_title",
        "channels_subtitle",
    )
    inlines = (ContactChannelInline,)


@admin.register(ContactChannel)
class ContactChannelAdmin(admin.ModelAdmin):
    list_display = ("name", "contacts_section", "sort_order", "is_active")
    list_filter = ("contacts_section", "is_active")
    search_fields = ("name", "href")
    list_editable = ("sort_order", "is_active")
    ordering = ("sort_order", "id")
