from django.contrib import admin

from apps.effectiveness.models import CompareItem, EffectivenessSection, TrainingItem


class TrainingItemInline(admin.TabularInline):
    model = TrainingItem
    extra = 1
    fields = ("title", "sort_order", "is_active")
    ordering = ("sort_order", "id")


class CompareItemInline(admin.TabularInline):
    model = CompareItem
    extra = 1
    fields = ("title", "ai_description", "human_description", "sort_order", "is_active")
    ordering = ("sort_order", "id")


@admin.register(EffectivenessSection)
class EffectivenessSectionAdmin(admin.ModelAdmin):
    list_display = ("id", "training_title", "summary_subtitle", "summary_title")
    search_fields = ("training_title", "summary_subtitle", "summary_title")
    inlines = (TrainingItemInline, CompareItemInline)


@admin.register(TrainingItem)
class TrainingItemAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "sort_order", "is_active")
    list_filter = ("section", "is_active")
    search_fields = ("title",)
    list_editable = ("sort_order", "is_active")
    ordering = ("sort_order", "id")


@admin.register(CompareItem)
class CompareItemAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "sort_order", "is_active")
    list_filter = ("section", "is_active")
    search_fields = ("title", "ai_description", "human_description")
    list_editable = ("sort_order", "is_active")
    ordering = ("sort_order", "id")
