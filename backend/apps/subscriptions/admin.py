from django.contrib import admin

from apps.subscriptions.models import SubscriptionItem, SubscriptionsSection


class SubscriptionItemInline(admin.TabularInline):
    model = SubscriptionItem
    extra = 1
    fields = ("text", "sort_order", "is_active")
    ordering = ("sort_order", "id")


@admin.register(SubscriptionsSection)
class SubscriptionsSectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "subtitle_prefix",
        "subtitle_highlight",
        "badge_primary",
        "badge_secondary",
    )
    search_fields = ("title", "subtitle_prefix", "subtitle_highlight", "badge_primary", "badge_secondary")
    inlines = (SubscriptionItemInline,)


@admin.register(SubscriptionItem)
class SubscriptionItemAdmin(admin.ModelAdmin):
    list_display = ("text", "section", "sort_order", "is_active")
    list_filter = ("section", "is_active")
    search_fields = ("text",)
    list_editable = ("sort_order", "is_active")
    ordering = ("sort_order", "id")
