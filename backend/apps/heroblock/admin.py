from django.contrib import admin

from apps.heroblock.models import HeroBlock, HeroStatItem


class HeroStatItemInline(admin.TabularInline):
    model = HeroStatItem
    extra = 1
    fields = ("value", "text", "sort_order", "is_active")
    ordering = ("sort_order", "id")


@admin.register(HeroBlock)
class HeroBlockAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "subtitle")
    search_fields = ("title", "subtitle", "description")
    inlines = (HeroStatItemInline,)


@admin.register(HeroStatItem)
class HeroStatItemAdmin(admin.ModelAdmin):
    list_display = ("value", "text", "sort_order", "is_active", "hero_block")
    list_filter = ("is_active", "hero_block")
    search_fields = ("value", "text")
    list_editable = ("sort_order", "is_active")
    ordering = ("sort_order", "id")
