from django.contrib import admin

from apps.integration_steps.models import IntegrationStepItem, IntegrationStepsSection


class IntegrationStepItemInline(admin.TabularInline):
    model = IntegrationStepItem
    extra = 1
    fields = ("day", "title", "description", "image", "sort_order", "is_active")
    ordering = ("sort_order", "id")


@admin.register(IntegrationStepsSection)
class IntegrationStepsSectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "subtitle",
        "cta_title_line_1",
        "cta_title_line_2",
    )
    search_fields = ("title", "subtitle", "cta_title_line_1", "cta_title_line_2")
    inlines = (IntegrationStepItemInline,)


@admin.register(IntegrationStepItem)
class IntegrationStepItemAdmin(admin.ModelAdmin):
    list_display = ("day", "title", "steps_section", "sort_order", "is_active")
    list_filter = ("steps_section", "is_active")
    search_fields = ("day", "title", "description")
    list_editable = ("sort_order", "is_active")
    ordering = ("sort_order", "id")
