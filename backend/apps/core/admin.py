from django.contrib import admin

from apps.core.models import HeaderMenuLink, SiteHeader

admin.site.site_header = "Администрирование CMS"
admin.site.site_title = "CMS"
admin.site.index_title = "Управление контентом"


class HeaderMenuLinkInline(admin.TabularInline):
    model = HeaderMenuLink
    extra = 1
    fields = ("title", "href", "sort_order", "is_active")
    ordering = ("sort_order", "id")


@admin.register(SiteHeader)
class SiteHeaderAdmin(admin.ModelAdmin):
    list_display = ("id", "brand_name", "logo_link")
    search_fields = ("brand_name", "logo_link")
    inlines = (HeaderMenuLinkInline,)


@admin.register(HeaderMenuLink)
class HeaderMenuLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "href", "sort_order", "is_active", "header")
    list_filter = ("is_active", "header")
    search_fields = ("title", "href")
    list_editable = ("sort_order", "is_active")
    ordering = ("sort_order", "id")
