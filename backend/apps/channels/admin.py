from django.contrib import admin

from apps.channels.models import ChannelItem, ChannelsSection


class ChannelItemInline(admin.TabularInline):
    model = ChannelItem
    extra = 1
    fields = ("name", "icon", "href", "sort_order", "is_active")
    ordering = ("sort_order", "id")


@admin.register(ChannelsSection)
class ChannelsSectionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "subtitle", "item_aria_label_prefix")
    search_fields = ("title", "subtitle", "description", "item_aria_label_prefix")
    inlines = (ChannelItemInline,)


@admin.register(ChannelItem)
class ChannelItemAdmin(admin.ModelAdmin):
    list_display = ("name", "section", "sort_order", "is_active")
    list_filter = ("section", "is_active")
    search_fields = ("name", "href")
    list_editable = ("sort_order", "is_active")
    ordering = ("sort_order", "id")
