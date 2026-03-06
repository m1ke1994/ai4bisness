from django.contrib import admin

from apps.system_integrations.models import SystemIntegrationItem, SystemIntegrationsSection


class SystemIntegrationItemInline(admin.TabularInline):
    model = SystemIntegrationItem
    extra = 1
    fields = ("title", "description", "image", "sort_order", "is_active")
    ordering = ("sort_order", "id")


@admin.register(SystemIntegrationsSection)
class SystemIntegrationsSectionAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title",)
    inlines = (SystemIntegrationItemInline,)


@admin.register(SystemIntegrationItem)
class SystemIntegrationItemAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "sort_order", "is_active")
    list_filter = ("section", "is_active")
    search_fields = ("title", "description")
    list_editable = ("sort_order", "is_active")
    ordering = ("sort_order", "id")
