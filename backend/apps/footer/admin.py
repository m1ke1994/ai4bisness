from django.contrib import admin

from apps.footer.models import FooterLink, SiteFooter


class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1
    fields = ("title", "href", "sort_order", "is_active")
    ordering = ("sort_order", "id")


@admin.register(SiteFooter)
class SiteFooterAdmin(admin.ModelAdmin):
    list_display = ("id", "brand_name", "logo_link")
    search_fields = ("brand_name", "logo_link")
    inlines = (FooterLinkInline,)


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "href", "sort_order", "is_active", "footer")
    list_filter = ("is_active", "footer")
    search_fields = ("title", "href")
    list_editable = ("sort_order", "is_active")
    ordering = ("sort_order", "id")
