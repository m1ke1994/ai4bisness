from django.contrib import admin
from django.utils.html import format_html

from apps.core.models import (
    AiIntegrationItem,
    AiValuePointItem,
    AiValueSection,
    AdvantagesAiSummaryItem,
    AdvantagesHumanLimitItem,
    AdvantagesSection,
    AdvantagesStatItem,
    ChannelItem,
    ChannelsSection,
    ComparisonRowItem,
    ContactEmail,
    ContactFormField,
    ContactMessenger,
    ContactPhone,
    ContactsSection,
    FooterColumn,
    FooterLink,
    FooterSection,
    HeaderMobileSocialItem,
    HeaderNavItem,
    HeaderSection,
    HeroLogoItem,
    HeroLogosSection,
    HeroSection,
    HeroStatItem,
    PolicyPage,
    PolicyParagraph,
    PolicySection,
    PricingPlan,
    PricingPlanFeature,
    PricingSection,
    ReviewDetailParagraph,
    ReviewItem,
    ReviewPreviewBullet,
    ReviewPreviewParagraph,
    ReviewResultItem,
    ReviewsSection,
    SiteSettings,
    StepCtaActionItem,
    StepItem,
    StepsSection,
    TrainingRightBulletItem,
    TrainingSourceItem,
)


admin.site.site_header = "Администрирование CMS"
admin.site.site_title = "CMS"
admin.site.index_title = "Управление контентом"


def image_preview(file_field, width: int = 80):
    if not file_field:
        return "-"
    return format_html(
        '<img src="{}" style="max-width:{}px;max-height:{}px;border-radius:6px;" />',
        file_field.url,
        width,
        width,
    )


class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    list_display = ("brand_name", "site_name", "support_email", "logo_preview", "updated_at")
    readonly_fields = ("logo_preview", "favicon_preview", "created_at", "updated_at")
    fieldsets = (
        (
            "Базовые настройки",
            {
                "fields": (
                    "brand_name",
                    "site_name",
                    "domain",
                    "description",
                    "locale",
                    "theme",
                    "support_email",
                    "contact_form_open_event",
                )
            },
        ),
        (
            "Медиа",
            {
                "fields": (
                    "logo",
                    "logo_alt",
                    "logo_preview",
                    "favicon",
                    "favicon_preview",
                )
            },
        ),
        ("Служебное", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Логотип")
    def logo_preview(self, obj):
        return image_preview(obj.logo)

    @admin.display(description="Фавикон")
    def favicon_preview(self, obj):
        return image_preview(obj.favicon)


class HeaderNavItemInline(admin.TabularInline):
    model = HeaderNavItem
    extra = 0
    fields = ("order", "is_active", "slug", "label", "href", "is_external")
    ordering = ("order", "id")


class HeaderMobileSocialInline(admin.TabularInline):
    model = HeaderMobileSocialItem
    extra = 0
    fields = ("order", "is_active", "slug", "label", "href", "aria_label", "icon", "icon_alt", "icon_preview")
    readonly_fields = ("icon_preview",)
    ordering = ("order", "id")

    @admin.display(description="Превью")
    def icon_preview(self, obj):
        return image_preview(obj.icon, width=40)


@admin.register(HeaderSection)
class HeaderSectionAdmin(SingletonAdmin):
    list_display = ("brand_href", "is_active", "updated_at")
    list_editable = ("is_active",)
    inlines = (HeaderNavItemInline, HeaderMobileSocialInline)
    fieldsets = (
        ("Базовое", {"fields": ("is_active", "brand_href")}),
        (
            "ARIA",
            {
                "fields": (
                    "aria_desktop_nav",
                    "aria_mobile_nav",
                    "aria_mobile_dialog",
                    "aria_open_menu",
                    "aria_close_menu",
                )
            },
        ),
        ("Служебное", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at")


class HeroStatInline(admin.TabularInline):
    model = HeroStatItem
    extra = 0
    fields = ("order", "is_active", "slug", "value", "text")
    ordering = ("order", "id")


@admin.register(HeroSection)
class HeroSectionAdmin(SingletonAdmin):
    list_display = ("title", "subtitle", "is_active", "phone_preview", "updated_at")
    list_editable = ("is_active",)
    readonly_fields = ("phone_preview", "texture_preview", "created_at", "updated_at")
    inlines = (HeroStatInline,)
    fieldsets = (
        (
            "Контент",
            {
                "fields": (
                    "is_active",
                    "title",
                    "subtitle",
                    "description",
                    "stats_disclaimer",
                    "image_vars",
                )
            },
        ),
        (
            "Медиа",
            {
                "fields": (
                    "phone_image",
                    "phone_alt",
                    "phone_preview",
                    "texture_image",
                    "texture_alt",
                    "texture_preview",
                )
            },
        ),
        ("Служебное", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Телефон")
    def phone_preview(self, obj):
        return image_preview(obj.phone_image)

    @admin.display(description="Текстура")
    def texture_preview(self, obj):
        return image_preview(obj.texture_image)


class HeroLogoInline(admin.TabularInline):
    model = HeroLogoItem
    extra = 0
    fields = ("order", "is_active", "slug", "logo", "logo_alt", "source_path", "logo_preview")
    readonly_fields = ("logo_preview",)
    ordering = ("order", "id")

    @admin.display(description="Превью")
    def logo_preview(self, obj):
        return image_preview(obj.logo)


@admin.register(HeroLogosSection)
class HeroLogosSectionAdmin(SingletonAdmin):
    list_display = ("is_active", "updated_at")
    inlines = (HeroLogoInline,)
    readonly_fields = ("created_at", "updated_at")

class AdvantagesStatInline(admin.TabularInline):
    model = AdvantagesStatItem
    extra = 0
    fields = ("order", "is_active", "slug", "value", "text")
    ordering = ("order", "id")


class TrainingSourceInline(admin.TabularInline):
    model = TrainingSourceItem
    extra = 0
    fields = ("order", "is_active", "slug", "title")
    ordering = ("order", "id")


class TrainingRightBulletInline(admin.TabularInline):
    model = TrainingRightBulletItem
    extra = 0
    fields = ("order", "is_active", "slug", "text")
    ordering = ("order", "id")


class ComparisonRowInline(admin.TabularInline):
    model = ComparisonRowItem
    extra = 0
    fields = ("order", "is_active", "slug", "title", "ai_description", "human_description")
    ordering = ("order", "id")


class AdvantagesAiSummaryInline(admin.TabularInline):
    model = AdvantagesAiSummaryItem
    extra = 0
    fields = ("order", "is_active", "slug", "text")
    ordering = ("order", "id")


class AdvantagesHumanLimitInline(admin.TabularInline):
    model = AdvantagesHumanLimitItem
    extra = 0
    fields = ("order", "is_active", "slug", "text")
    ordering = ("order", "id")


@admin.register(AdvantagesSection)
class AdvantagesSectionAdmin(SingletonAdmin):
    list_display = ("training_badge", "summary_title", "is_active", "check_icon_preview", "updated_at")
    list_editable = ("is_active",)
    readonly_fields = ("check_icon_preview", "created_at", "updated_at")
    inlines = (
        AdvantagesStatInline,
        TrainingSourceInline,
        TrainingRightBulletInline,
        ComparisonRowInline,
        AdvantagesAiSummaryInline,
        AdvantagesHumanLimitInline,
    )
    fieldsets = (
        (
            "Обучение",
            {
                "fields": (
                    "is_active",
                    "training_badge",
                    "training_right_pill",
                    "training_right_title",
                    "check_icon",
                    "check_icon_alt",
                    "check_icon_preview",
                )
            },
        ),
        (
            "Сравнение",
            {
                "fields": (
                    "summary_title",
                    "summary_subtitle",
                    "summary_description",
                    "desktop_stage_label",
                    "desktop_ai_label",
                    "desktop_human_label",
                    "mobile_title",
                    "mobile_subtitle",
                    "mobile_ai_label",
                    "mobile_human_label",
                    "mobile_footer",
                    "stage_description_label",
                )
            },
        ),
        ("Служебное", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Иконка")
    def check_icon_preview(self, obj):
        return image_preview(obj.check_icon)


class AiValuePointInline(admin.TabularInline):
    model = AiValuePointItem
    extra = 0
    fields = ("order", "is_active", "slug", "text")


class AiIntegrationInline(admin.TabularInline):
    model = AiIntegrationItem
    extra = 0
    fields = ("order", "is_active", "slug", "title", "description", "image", "image_alt", "source_path", "image_preview")
    readonly_fields = ("image_preview",)

    @admin.display(description="Превью")
    def image_preview(self, obj):
        return image_preview(obj.image)


@admin.register(AiValueSection)
class AiValueSectionAdmin(SingletonAdmin):
    list_display = ("title", "is_active", "integrations_banner_preview", "updated_at")
    list_editable = ("is_active",)
    readonly_fields = ("integrations_banner_preview", "created_at", "updated_at")
    inlines = (AiValuePointInline, AiIntegrationInline)
    fieldsets = (
        (
            "Контент",
            {
                "fields": (
                    "is_active",
                    "title",
                    "subtitle_prefix",
                    "subtitle_highlight",
                    "description",
                )
            },
        ),
        (
            "Блок Launch",
            {
                "fields": (
                    "launch_badge_primary",
                    "launch_badge_secondary",
                    "launch_title",
                    "launch_description",
                    "launch_left_label",
                    "launch_right_label",
                    "launch_paid_title",
                    "launch_paid_description",
                    "launch_note_title",
                    "launch_note_description",
                )
            },
        ),
        (
            "Интеграции",
            {
                "fields": (
                    "integrations_title",
                    "integrations_subtitle",
                    "integrations_add_aria_label",
                    "integrations_banner",
                    "integrations_banner_alt",
                    "integrations_banner_preview",
                )
            },
        ),
        ("Служебное", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Баннер")
    def integrations_banner_preview(self, obj):
        return image_preview(obj.integrations_banner)


class ChannelItemInline(admin.TabularInline):
    model = ChannelItem
    extra = 0
    fields = ("order", "is_active", "slug", "name", "href", "icon", "icon_alt", "icon_preview")
    readonly_fields = ("icon_preview",)

    @admin.display(description="Превью")
    def icon_preview(self, obj):
        return image_preview(obj.icon, width=40)


@admin.register(ChannelsSection)
class ChannelsSectionAdmin(SingletonAdmin):
    list_display = ("title", "subtitle", "is_active", "updated_at")
    list_editable = ("is_active",)
    readonly_fields = (
        "background_preview",
        "primary_phone_preview",
        "secondary_phone_preview",
        "created_at",
        "updated_at",
    )
    inlines = (ChannelItemInline,)
    fieldsets = (
        ("Контент", {"fields": ("is_active", "title", "subtitle", "description", "item_aria_label_prefix")}),
        (
            "Медиа",
            {
                "fields": (
                    "background_image",
                    "background_alt",
                    "background_preview",
                    "primary_phone_image",
                    "primary_phone_alt",
                    "primary_phone_preview",
                    "secondary_phone_image",
                    "secondary_phone_alt",
                    "secondary_phone_preview",
                )
            },
        ),
        ("Служебное", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Фон")
    def background_preview(self, obj):
        return image_preview(obj.background_image)

    @admin.display(description="Телефон 1")
    def primary_phone_preview(self, obj):
        return image_preview(obj.primary_phone_image)

    @admin.display(description="Телефон 2")
    def secondary_phone_preview(self, obj):
        return image_preview(obj.secondary_phone_image)


class StepItemInline(admin.TabularInline):
    model = StepItem
    extra = 0
    fields = ("order", "is_active", "slug", "day", "title", "description", "image", "image_alt", "source_path", "image_preview")
    readonly_fields = ("image_preview",)

    @admin.display(description="Превью")
    def image_preview(self, obj):
        return image_preview(obj.image)


class StepCtaActionInline(admin.TabularInline):
    model = StepCtaActionItem
    extra = 0
    fields = ("order", "is_active", "slug", "label", "href", "aria_label", "is_external")


@admin.register(StepsSection)
class StepsSectionAdmin(SingletonAdmin):
    list_display = ("title", "subtitle", "is_active", "updated_at")
    list_editable = ("is_active",)
    readonly_fields = ("cta_image_preview", "cta_background_preview", "created_at", "updated_at")
    inlines = (StepItemInline, StepCtaActionInline)
    fieldsets = (
        (
            "Контент",
            {
                "fields": (
                    "is_active",
                    "title",
                    "subtitle",
                    "cta_title",
                    "cta_button_label",
                    "cta_button_href",
                )
            },
        ),
        (
            "CTA медиа",
            {
                "fields": (
                    "cta_image",
                    "cta_image_alt",
                    "cta_image_source_path",
                    "cta_image_preview",
                    "cta_background_image",
                    "cta_background_alt",
                    "cta_background_preview",
                )
            },
        ),
        ("Служебное", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="CTA изображение")
    def cta_image_preview(self, obj):
        return image_preview(obj.cta_image)

    @admin.display(description="CTA фон")
    def cta_background_preview(self, obj):
        return image_preview(obj.cta_background_image)


class PricingPlanInline(admin.TabularInline):
    model = PricingPlan
    extra = 0
    fields = (
        "order",
        "is_active",
        "slug",
        "title",
        "subtitle",
        "channels",
        "accent_badge",
        "inherit_line",
        "featured",
        "dark_card",
        "cta_label",
        "cta_href",
    )


@admin.register(PricingSection)
class PricingSectionAdmin(SingletonAdmin):
    list_display = ("title", "subtitle", "channels_label", "is_active", "updated_at")
    list_editable = ("is_active",)
    inlines = (PricingPlanInline,)
    readonly_fields = ("created_at", "updated_at")


class PricingPlanFeatureInline(admin.TabularInline):
    model = PricingPlanFeature
    extra = 0
    fields = ("order", "is_active", "slug", "text")


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "order", "is_active", "featured", "dark_card")
    list_filter = ("section", "is_active", "featured", "dark_card")
    list_editable = ("order", "is_active", "featured", "dark_card")
    inlines = (PricingPlanFeatureInline,)

class ReviewPreviewParagraphInline(admin.TabularInline):
    model = ReviewPreviewParagraph
    extra = 0
    fields = ("order", "is_active", "slug", "text")


class ReviewPreviewBulletInline(admin.TabularInline):
    model = ReviewPreviewBullet
    extra = 0
    fields = ("order", "is_active", "slug", "text")


class ReviewDetailParagraphInline(admin.TabularInline):
    model = ReviewDetailParagraph
    extra = 0
    fields = ("order", "is_active", "slug", "text")


class ReviewResultInline(admin.TabularInline):
    model = ReviewResultItem
    extra = 0
    fields = ("order", "is_active", "slug", "text")


class ReviewItemInline(admin.TabularInline):
    model = ReviewItem
    extra = 0
    fields = ("order", "is_active", "slug", "company", "person", "rating")


@admin.register(ReviewsSection)
class ReviewsSectionAdmin(SingletonAdmin):
    list_display = ("title", "subtitle", "is_active", "updated_at")
    list_editable = ("is_active",)
    inlines = (ReviewItemInline,)
    readonly_fields = ("created_at", "updated_at")


@admin.register(ReviewItem)
class ReviewItemAdmin(admin.ModelAdmin):
    list_display = ("company", "section", "order", "is_active")
    list_filter = ("section", "is_active")
    list_editable = ("order", "is_active")
    inlines = (ReviewPreviewParagraphInline, ReviewPreviewBulletInline, ReviewDetailParagraphInline, ReviewResultInline)


class ContactMessengerInline(admin.TabularInline):
    model = ContactMessenger
    extra = 0
    fields = (
        "order",
        "is_active",
        "slug",
        "name",
        "label",
        "href",
        "icon",
        "icon_alt",
        "icon_preview",
        "aria_label",
        "message",
        "is_external",
    )
    readonly_fields = ("icon_preview",)

    @admin.display(description="Превью")
    def icon_preview(self, obj):
        return image_preview(obj.icon, width=40)


class ContactFormFieldInline(admin.TabularInline):
    model = ContactFormField
    extra = 0
    fields = ("order", "is_active", "slug", "field_key", "label", "placeholder", "field_type", "is_required")


class ContactPhoneInline(admin.TabularInline):
    model = ContactPhone
    extra = 0
    fields = ("order", "is_active", "slug", "label", "value", "href")


class ContactEmailInline(admin.TabularInline):
    model = ContactEmail
    extra = 0
    fields = ("order", "is_active", "slug", "label", "value", "href")


@admin.register(ContactsSection)
class ContactsSectionAdmin(SingletonAdmin):
    list_display = ("title", "subtitle", "is_active", "updated_at")
    list_editable = ("is_active",)
    readonly_fields = ("section_background_preview", "card_background_preview", "created_at", "updated_at")
    inlines = (ContactMessengerInline, ContactFormFieldInline, ContactPhoneInline, ContactEmailInline)
    fieldsets = (
        (
            "Контент",
            {
                "fields": (
                    "is_active",
                    "title",
                    "subtitle",
                    "heading_line3",
                    "description",
                    "card_title_line1",
                    "card_title_line2",
                    "card_response_time",
                    "form_title",
                    "form_subtitle",
                    "form_submit_label",
                    "form_close_aria_label",
                )
            },
        ),
        (
            "Медиа",
            {
                "fields": (
                    "section_background_image",
                    "section_background_alt",
                    "section_background_preview",
                    "card_background_image",
                    "card_background_alt",
                    "card_background_preview",
                )
            },
        ),
        ("Служебное", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Фон секции")
    def section_background_preview(self, obj):
        return image_preview(obj.section_background_image)

    @admin.display(description="Фон карточки")
    def card_background_preview(self, obj):
        return image_preview(obj.card_background_image)


class FooterColumnInline(admin.TabularInline):
    model = FooterColumn
    extra = 0
    fields = ("order", "is_active", "slug", "title")


@admin.register(FooterSection)
class FooterSectionAdmin(SingletonAdmin):
    list_display = ("brand_name", "brand_href", "support_email", "is_active", "logo_preview", "updated_at")
    list_editable = ("is_active",)
    readonly_fields = ("logo_preview", "created_at", "updated_at")
    inlines = (FooterColumnInline,)

    @admin.display(description="Логотип")
    def logo_preview(self, obj):
        return image_preview(obj.logo)


class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 0
    fields = ("order", "is_active", "slug", "label", "href", "is_external")


@admin.register(FooterColumn)
class FooterColumnAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("section", "is_active")
    inlines = (FooterLinkInline,)


class PolicySectionInline(admin.TabularInline):
    model = PolicySection
    extra = 0
    fields = ("order", "is_active", "slug", "title")


@admin.register(PolicyPage)
class PolicyPageAdmin(admin.ModelAdmin):
    list_display = ("slug", "title", "is_active", "updated_at")
    list_editable = ("is_active",)
    inlines = (PolicySectionInline,)


class PolicyParagraphInline(admin.TabularInline):
    model = PolicyParagraph
    extra = 0
    fields = ("order", "is_active", "slug", "text")


@admin.register(PolicySection)
class PolicySectionAdmin(admin.ModelAdmin):
    list_display = ("title", "page", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("page", "is_active")
    inlines = (PolicyParagraphInline,)


@admin.register(PolicyParagraph)
class PolicyParagraphAdmin(admin.ModelAdmin):
    list_display = ("short_text", "section", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("section", "is_active")

    @admin.display(description="Текст")
    def short_text(self, obj):
        return obj.text[:80]


# Регистрация item-моделей, которые не имеют собственного админ-класса.
for model in (
    HeaderNavItem,
    HeaderMobileSocialItem,
    HeroStatItem,
    HeroLogoItem,
    AdvantagesStatItem,
    TrainingSourceItem,
    TrainingRightBulletItem,
    ComparisonRowItem,
    AdvantagesAiSummaryItem,
    AdvantagesHumanLimitItem,
    AiValuePointItem,
    AiIntegrationItem,
    ChannelItem,
    StepItem,
    StepCtaActionItem,
    PricingPlanFeature,
    ReviewPreviewParagraph,
    ReviewPreviewBullet,
    ReviewDetailParagraph,
    ReviewResultItem,
    ContactMessenger,
    ContactFormField,
    ContactPhone,
    ContactEmail,
    FooterLink,
):
    if model not in admin.site._registry:
        admin.site.register(model)
