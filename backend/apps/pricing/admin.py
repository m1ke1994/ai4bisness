from django.contrib import admin

from apps.pricing.models import PricingFeature, PricingPlan, PricingSection


class PricingPlanInline(admin.TabularInline):
    model = PricingPlan
    extra = 1
    fields = (
        "title",
        "subtitle",
        "accent_badge",
        "inherit_line",
        "channels",
        "cta_label",
        "cta_link",
        "sort_order",
        "is_active",
        "is_featured",
        "is_dark_card",
    )
    ordering = ("sort_order", "id")


class PricingFeatureInline(admin.TabularInline):
    model = PricingFeature
    extra = 1
    fields = ("text", "sort_order", "is_active")
    ordering = ("sort_order", "id")


@admin.register(PricingSection)
class PricingSectionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "subtitle", "channels_label")
    search_fields = ("title", "subtitle", "channels_label")
    inlines = (PricingPlanInline,)


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "pricing_section",
        "sort_order",
        "is_active",
        "is_featured",
        "is_dark_card",
    )
    list_filter = ("pricing_section", "is_active", "is_featured", "is_dark_card")
    search_fields = ("title", "subtitle", "channels", "cta_label", "cta_link")
    list_editable = ("sort_order", "is_active", "is_featured", "is_dark_card")
    ordering = ("sort_order", "id")
    inlines = (PricingFeatureInline,)


@admin.register(PricingFeature)
class PricingFeatureAdmin(admin.ModelAdmin):
    list_display = ("text", "plan", "sort_order", "is_active")
    list_filter = ("plan", "is_active")
    search_fields = ("text",)
    list_editable = ("sort_order", "is_active")
    ordering = ("sort_order", "id")
