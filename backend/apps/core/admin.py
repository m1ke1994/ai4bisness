from django.contrib import admin

from apps.core.models import HeaderNavItem, HeaderSection, HeaderSocialLink


class HeaderNavItemInline(admin.TabularInline):
    model = HeaderNavItem
    fields = ("label", "href", "sort_order", "is_active")
    extra = 0


class HeaderSocialLinkInline(admin.TabularInline):
    model = HeaderSocialLink
    fields = ("href", "aria_label", "icon_image", "icon_url", "icon_alt", "sort_order", "is_active")
    extra = 0


@admin.register(HeaderSection)
class HeaderSectionAdmin(admin.ModelAdmin):
    list_display = ("is_enabled", "brand_name", "brand_href", "updated_at")
    list_filter = ("is_enabled",)
    search_fields = ("brand_name", "brand_href")
    readonly_fields = ("created_at", "updated_at")
    inlines = (HeaderNavItemInline, HeaderSocialLinkInline)
    fieldsets = (
        (
            "Бренд",
            {
                "fields": ("is_enabled", "brand_name", "brand_href", "logo_image", "logo_url", "logo_alt"),
            },
        ),
        (
            "ARIA подписи",
            {
                "fields": (
                    "desktop_nav_aria",
                    "mobile_dialog_aria",
                    "mobile_nav_aria",
                    "open_menu_aria",
                    "close_menu_aria",
                ),
            },
        ),
        (
            "Служебное",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )


@admin.register(HeaderNavItem)
class HeaderNavItemAdmin(admin.ModelAdmin):
    list_display = ("label", "href", "sort_order", "is_active", "header")
    list_filter = ("is_active", "header")
    search_fields = ("label", "href")
    ordering = ("sort_order", "id")


@admin.register(HeaderSocialLink)
class HeaderSocialLinkAdmin(admin.ModelAdmin):
    list_display = ("aria_label", "href", "sort_order", "is_active", "header")
    list_filter = ("is_active", "header")
    search_fields = ("aria_label", "href")
    ordering = ("sort_order", "id")
