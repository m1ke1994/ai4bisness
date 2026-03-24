from django.contrib import admin

from apps.company_briefs.models import CompanyBrief


@admin.register(CompanyBrief)
class CompanyBriefAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "company_name",
        "industry",
        "primary_email",
        "created_at",
        "telegram_status",
    )
    list_filter = ("telegram_status", "industry", "created_at")
    search_fields = ("company_name", "industry", "primary_email", "city", "country")
    readonly_fields = (
        "company_name",
        "industry",
        "subindustry",
        "team_members",
        "short_description",
        "full_description",
        "primary_phone",
        "secondary_phone",
        "primary_email",
        "support_email",
        "sales_email",
        "address",
        "city",
        "country",
        "website_url",
        "timezone_name",
        "services",
        "assistant_channels",
        "crm_integrations",
        "booking_integrations",
        "pdf_file",
        "telegram_status",
        "telegram_error",
        "source_ip",
        "created_at",
    )
    fieldsets = (
        (
            "Основные",
            {
                "fields": (
                    "company_name",
                    "industry",
                    "subindustry",
                    "team_members",
                    "short_description",
                    "full_description",
                )
            },
        ),
        (
            "Контакты",
            {
                "fields": (
                    "primary_phone",
                    "secondary_phone",
                    "primary_email",
                    "support_email",
                    "sales_email",
                    "address",
                    "city",
                    "country",
                    "website_url",
                    "timezone_name",
                )
            },
        ),
        ("Услуги", {"fields": ("services",)}),
        ("Ассистенты и интеграции", {"fields": ("assistant_channels", "crm_integrations", "booking_integrations")}),
        ("Система", {"fields": ("pdf_file", "telegram_status", "telegram_error", "source_ip", "created_at")}),
    )
