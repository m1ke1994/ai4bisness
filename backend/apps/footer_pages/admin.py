from django.contrib import admin

from apps.footer_pages.models import FooterPage


@admin.register(FooterPage)
class FooterPageAdmin(admin.ModelAdmin):
    list_display = ("title", "key", "slug", "is_published", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title", "content", "slug", "key")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("key", "id")
    fieldsets = (
        (
            "Основная информация",
            {
                "fields": ("title", "key", "slug"),
            },
        ),
        (
            "Содержимое",
            {
                "fields": ("content",),
            },
        ),
        (
            "Публикация",
            {
                "fields": ("is_published",),
            },
        ),
        (
            "Служебная информация",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

