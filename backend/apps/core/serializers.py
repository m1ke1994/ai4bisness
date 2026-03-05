from __future__ import annotations

from typing import Any

from rest_framework import serializers

from apps.core.models import (
    AiIntegrationItem,
    AiValuePointItem,
    AiValueSection,
    AdvantagesAiSummaryItem,
    AdvantagesHumanLimitItem,
    AdvantagesSection,
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


class MediaUrlMixin:
    def absolute_media(self, file_field, fallback: str = "") -> str:
        value = fallback or ""
        if file_field and getattr(file_field, "name", ""):
            value = file_field.url
        request = self.context.get("request")
        if request and value and value.startswith("/"):
            return request.build_absolute_uri(value)
        return value


class OrderedItemSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    sortOrder = serializers.IntegerField(source="order")
    isActive = serializers.BooleanField(source="is_active")

    id_prefix = "item"

    def get_id(self, obj) -> str:
        return obj.slug or f"{self.id_prefix}-{obj.pk}"


class HeaderNavItemSerializer(OrderedItemSerializer):
    id_prefix = "nav"

    class Meta:
        model = HeaderNavItem
        fields = ("id", "slug", "label", "href", "sortOrder", "isActive")


class HeaderMobileSocialSerializer(MediaUrlMixin, OrderedItemSerializer):
    id_prefix = "mobile-social"
    ariaLabel = serializers.CharField(source="aria_label")
    icon = serializers.SerializerMethodField()

    class Meta:
        model = HeaderMobileSocialItem
        fields = ("id", "slug", "label", "href", "ariaLabel", "icon", "sortOrder", "isActive")

    def get_icon(self, obj) -> dict[str, str]:
        return {
            "src": self.absolute_media(obj.icon),
            "alt": obj.icon_alt or obj.label,
        }


class HeroStatSerializer(OrderedItemSerializer):
    id_prefix = "hero-stat"

    class Meta:
        model = HeroStatItem
        fields = ("id", "slug", "value", "text", "sortOrder", "isActive")


class HeroLogoSerializer(MediaUrlMixin, OrderedItemSerializer):
    id_prefix = "hero-logo"
    src = serializers.SerializerMethodField()
    alt = serializers.CharField(source="logo_alt")

    class Meta:
        model = HeroLogoItem
        fields = ("id", "slug", "src", "alt", "sortOrder", "isActive")

    def get_src(self, obj) -> str:
        return self.absolute_media(obj.logo, fallback=obj.source_path)


class TrainingSourceSerializer(OrderedItemSerializer):
    id_prefix = "training-source"

    class Meta:
        model = TrainingSourceItem
        fields = ("id", "slug", "title", "sortOrder", "isActive")


class TextItemSerializer(OrderedItemSerializer):
    id_prefix = "text-item"

    class Meta:
        fields = ("id", "slug", "text", "sortOrder", "isActive")


class TrainingRightBulletSerializer(TextItemSerializer):
    id_prefix = "training-right-bullet"

    class Meta(TextItemSerializer.Meta):
        model = TrainingRightBulletItem


class ComparisonRowSerializer(OrderedItemSerializer):
    id_prefix = "comparison-row"
    aiDescription = serializers.CharField(source="ai_description")
    humanDescription = serializers.CharField(source="human_description")

    class Meta:
        model = ComparisonRowItem
        fields = (
            "id",
            "slug",
            "title",
            "aiDescription",
            "humanDescription",
            "sortOrder",
            "isActive",
        )


class AiSummarySerializer(TextItemSerializer):
    id_prefix = "ai-summary"

    class Meta(TextItemSerializer.Meta):
        model = AdvantagesAiSummaryItem


class HumanLimitSerializer(TextItemSerializer):
    id_prefix = "human-limit"

    class Meta(TextItemSerializer.Meta):
        model = AdvantagesHumanLimitItem


class AiValuePointSerializer(TextItemSerializer):
    id_prefix = "ai-value-point"

    class Meta(TextItemSerializer.Meta):
        model = AiValuePointItem


class AiIntegrationSerializer(MediaUrlMixin, OrderedItemSerializer):
    id_prefix = "integration-row"
    media = serializers.SerializerMethodField()

    class Meta:
        model = AiIntegrationItem
        fields = ("id", "slug", "title", "description", "media", "sortOrder", "isActive")

    def get_media(self, obj) -> dict[str, Any]:
        return {
            "image": {
                "src": self.absolute_media(obj.image, fallback=obj.source_path),
                "alt": obj.image_alt or obj.title,
            }
        }

class ChannelItemSerializer(MediaUrlMixin, OrderedItemSerializer):
    id_prefix = "channel"
    icon = serializers.SerializerMethodField()

    class Meta:
        model = ChannelItem
        fields = ("id", "slug", "name", "href", "icon", "sortOrder", "isActive")

    def get_icon(self, obj) -> dict[str, str]:
        return {
            "src": self.absolute_media(obj.icon),
            "alt": obj.icon_alt or obj.name,
        }


class StepItemSerializer(MediaUrlMixin, OrderedItemSerializer):
    id_prefix = "step"
    media = serializers.SerializerMethodField()

    class Meta:
        model = StepItem
        fields = ("id", "slug", "day", "title", "description", "media", "sortOrder", "isActive")

    def get_media(self, obj) -> dict[str, Any]:
        return {
            "image": {
                "src": self.absolute_media(obj.image, fallback=obj.source_path),
                "alt": obj.image_alt or obj.title,
            }
        }


class StepCtaActionSerializer(OrderedItemSerializer):
    id_prefix = "steps-cta"
    ariaLabel = serializers.CharField(source="aria_label")

    class Meta:
        model = StepCtaActionItem
        fields = ("id", "slug", "label", "href", "ariaLabel", "sortOrder", "isActive")


class PricingPlanFeatureSerializer(TextItemSerializer):
    id_prefix = "pricing-feature"

    class Meta(TextItemSerializer.Meta):
        model = PricingPlanFeature


class PricingPlanSerializer(OrderedItemSerializer):
    id_prefix = "pricing"
    meta = serializers.SerializerMethodField()
    cta = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    accentBadge = serializers.CharField(source="accent_badge")
    inheritLine = serializers.CharField(source="inherit_line")

    class Meta:
        model = PricingPlan
        fields = (
            "id",
            "slug",
            "title",
            "subtitle",
            "channels",
            "accentBadge",
            "inheritLine",
            "meta",
            "cta",
            "features",
            "sortOrder",
            "isActive",
        )

    def get_meta(self, obj) -> dict[str, bool]:
        return {
            "featured": obj.featured,
            "darkCard": obj.dark_card,
        }

    def get_cta(self, obj) -> dict[str, Any]:
        return {
            "id": f"{obj.slug or obj.pk}-cta",
            "slug": f"{obj.slug or obj.pk}-cta",
            "label": obj.cta_label,
            "href": obj.cta_href,
            "sortOrder": 1,
            "isActive": True,
        }

    def get_features(self, obj):
        queryset = obj.features.filter(is_active=True).order_by("order", "id")
        serializer = PricingPlanFeatureSerializer(queryset, many=True, context=self.context)
        return serializer.data


class ReviewTextItemSerializer(TextItemSerializer):
    id_prefix = "review-text"


class ReviewPreviewParagraphSerializer(ReviewTextItemSerializer):
    id_prefix = "review-preview-paragraph"

    class Meta(ReviewTextItemSerializer.Meta):
        model = ReviewPreviewParagraph


class ReviewPreviewBulletSerializer(ReviewTextItemSerializer):
    id_prefix = "review-preview-bullet"

    class Meta(ReviewTextItemSerializer.Meta):
        model = ReviewPreviewBullet


class ReviewDetailParagraphSerializer(ReviewTextItemSerializer):
    id_prefix = "review-detail-paragraph"

    class Meta(ReviewTextItemSerializer.Meta):
        model = ReviewDetailParagraph


class ReviewResultSerializer(ReviewTextItemSerializer):
    id_prefix = "review-result"

    class Meta(ReviewTextItemSerializer.Meta):
        model = ReviewResultItem


class ReviewItemSerializer(OrderedItemSerializer):
    id_prefix = "review"
    previewParagraphs = serializers.SerializerMethodField()
    previewBullets = serializers.SerializerMethodField()
    detailsParagraphs = serializers.SerializerMethodField()
    results = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()

    class Meta:
        model = ReviewItem
        fields = (
            "id",
            "slug",
            "company",
            "person",
            "previewParagraphs",
            "previewBullets",
            "detailsParagraphs",
            "results",
            "media",
            "meta",
            "sortOrder",
            "isActive",
        )

    def get_previewParagraphs(self, obj):
        qs = obj.preview_paragraphs.filter(is_active=True).order_by("order", "id")
        return ReviewPreviewParagraphSerializer(qs, many=True, context=self.context).data

    def get_previewBullets(self, obj):
        qs = obj.preview_bullets.filter(is_active=True).order_by("order", "id")
        return ReviewPreviewBulletSerializer(qs, many=True, context=self.context).data

    def get_detailsParagraphs(self, obj):
        qs = obj.detail_paragraphs.filter(is_active=True).order_by("order", "id")
        return ReviewDetailParagraphSerializer(qs, many=True, context=self.context).data

    def get_results(self, obj):
        qs = obj.results.filter(is_active=True).order_by("order", "id")
        return ReviewResultSerializer(qs, many=True, context=self.context).data

    def get_media(self, obj) -> dict[str, Any]:
        return {}

    def get_meta(self, obj) -> dict[str, Any]:
        return {"rating": obj.rating}


class ContactMessengerSerializer(MediaUrlMixin, OrderedItemSerializer):
    id_prefix = "messenger"
    icon = serializers.SerializerMethodField()
    ariaLabel = serializers.CharField(source="aria_label")

    class Meta:
        model = ContactMessenger
        fields = (
            "id",
            "slug",
            "name",
            "label",
            "href",
            "icon",
            "ariaLabel",
            "sortOrder",
            "isActive",
        )

    def get_icon(self, obj) -> dict[str, str]:
        return {
            "src": self.absolute_media(obj.icon),
            "alt": obj.icon_alt or obj.label,
        }


class ContactFormFieldSerializer(OrderedItemSerializer):
    id_prefix = "contacts-form"
    key = serializers.CharField(source="field_key")
    type = serializers.CharField(source="field_type")
    required = serializers.BooleanField(source="is_required")

    class Meta:
        model = ContactFormField
        fields = (
            "id",
            "slug",
            "key",
            "label",
            "placeholder",
            "type",
            "required",
            "sortOrder",
            "isActive",
        )


class ContactPhoneSerializer(OrderedItemSerializer):
    id_prefix = "contact-phone"

    class Meta:
        model = ContactPhone
        fields = ("id", "slug", "label", "value", "href", "sortOrder", "isActive")


class ContactEmailSerializer(OrderedItemSerializer):
    id_prefix = "contact-email"

    class Meta:
        model = ContactEmail
        fields = ("id", "slug", "label", "value", "href", "sortOrder", "isActive")


class FooterLinkSerializer(OrderedItemSerializer):
    id_prefix = "footer-link"

    class Meta:
        model = FooterLink
        fields = ("id", "slug", "label", "href", "sortOrder", "isActive")


class FooterColumnSerializer(OrderedItemSerializer):
    id_prefix = "footer-column"
    links = serializers.SerializerMethodField()

    class Meta:
        model = FooterColumn
        fields = ("id", "slug", "title", "links", "sortOrder", "isActive")

    def get_links(self, obj):
        qs = obj.links.filter(is_active=True).order_by("order", "id")
        return FooterLinkSerializer(qs, many=True, context=self.context).data


class PolicyParagraphSerializer(OrderedItemSerializer):
    id_prefix = "policy-paragraph"

    class Meta:
        model = PolicyParagraph
        fields = ("id", "slug", "text", "sortOrder", "isActive")


class PolicySectionSerializer(OrderedItemSerializer):
    id_prefix = "policy-section"
    paragraphs = serializers.SerializerMethodField()

    class Meta:
        model = PolicySection
        fields = ("id", "slug", "title", "paragraphs", "sortOrder", "isActive")

    def get_paragraphs(self, obj):
        qs = obj.paragraphs.filter(is_active=True).order_by("order", "id")
        return PolicyParagraphSerializer(qs, many=True, context=self.context).data


class PolicyPageSerializer(serializers.ModelSerializer):
    sections = serializers.SerializerMethodField()

    class Meta:
        model = PolicyPage
        fields = ("slug", "title", "back_button_label", "is_active", "sections")

    def get_sections(self, obj):
        qs = obj.sections.filter(is_active=True).order_by("order", "id")
        return PolicySectionSerializer(qs, many=True, context=self.context).data

class SiteSettingsSerializer(MediaUrlMixin, serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    favicon = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = (
            "brand_name",
            "site_name",
            "domain",
            "description",
            "locale",
            "theme",
            "support_email",
            "contact_form_open_event",
            "logo",
            "favicon",
        )

    def get_logo(self, obj) -> dict[str, str]:
        return {
            "src": self.absolute_media(obj.logo),
            "alt": obj.logo_alt or obj.brand_name,
        }

    def get_favicon(self, obj) -> dict[str, str]:
        return {
            "src": self.absolute_media(obj.favicon),
            "alt": obj.brand_name,
        }


class HeaderSectionSerializer(MediaUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = HeaderSection
        fields = (
            "brand_href",
            "aria_desktop_nav",
            "aria_mobile_nav",
            "aria_mobile_dialog",
            "aria_open_menu",
            "aria_close_menu",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        settings = SiteSettings.objects.first()
        nav_items = instance.nav_items.filter(is_active=True).order_by("order", "id")
        mobile_socials = instance.mobile_social_items.filter(is_active=True).order_by("order", "id")
        return {
            "id": "nav",
            "items": HeaderNavItemSerializer(nav_items, many=True, context=self.context).data,
            "cta": None,
            "media": {
                "logo": {
                    "src": self.absolute_media(settings.logo if settings else None),
                    "alt": (settings.logo_alt if settings else "") or (settings.brand_name if settings else ""),
                }
            },
            "meta": {
                "brandHref": data["brand_href"],
                "aria": {
                    "desktopNav": data["aria_desktop_nav"],
                    "mobileNav": data["aria_mobile_nav"],
                    "mobileDialog": data["aria_mobile_dialog"],
                    "openMenu": data["aria_open_menu"],
                    "closeMenu": data["aria_close_menu"],
                },
                "mobileSocials": HeaderMobileSocialSerializer(mobile_socials, many=True, context=self.context).data,
            },
        }


class HeroSectionSerializer(MediaUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = (
            "title",
            "subtitle",
            "description",
            "stats_disclaimer",
            "phone_alt",
            "image_vars",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        stats = instance.stats.filter(is_active=True).order_by("order", "id")
        return {
            "id": "hero",
            "title": data["title"],
            "subtitle": data["subtitle"],
            "description": data["description"],
            "items": HeroStatSerializer(stats, many=True, context=self.context).data,
            "cta": None,
            "media": {
                "image": {
                    "src": self.absolute_media(instance.phone_image),
                    "alt": instance.phone_alt,
                },
                "texture": {
                    "src": self.absolute_media(instance.texture_image),
                    "alt": instance.texture_alt,
                },
            },
            "meta": {
                "statsDisclaimer": data["stats_disclaimer"],
                "imageVars": data["image_vars"] or {},
            },
        }


class HeroLogosSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroLogosSection
        fields = ()

    def to_representation(self, instance):
        logos = instance.items.filter(is_active=True).order_by("order", "id")
        return {
            "id": "hero-logos",
            "items": HeroLogoSerializer(logos, many=True, context=self.context).data,
            "cta": None,
            "media": {},
            "meta": {},
        }


class AdvantagesSectionSerializer(MediaUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = AdvantagesSection
        fields = (
            "training_badge",
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
            "training_right_pill",
            "training_right_title",
        )

    def to_representation(self, instance):
        base = super().to_representation(instance)
        rows = instance.comparison_rows.filter(is_active=True).order_by("order", "id")
        sources = instance.training_sources.filter(is_active=True).order_by("order", "id")
        bullets = instance.training_right_bullets.filter(is_active=True).order_by("order", "id")
        ai_summary = instance.ai_summary_items.filter(is_active=True).order_by("order", "id")
        human_limits = instance.human_limit_items.filter(is_active=True).order_by("order", "id")

        return {
            "id": "advantages",
            "title": base["training_badge"],
            "subtitle": base["summary_title"],
            "description": base["summary_description"],
            "items": ComparisonRowSerializer(rows, many=True, context=self.context).data,
            "cta": None,
            "media": {
                "icon": {
                    "src": self.absolute_media(instance.check_icon),
                    "alt": instance.check_icon_alt,
                }
            },
            "meta": {
                "training": {
                    "id": "advantages-training",
                    "title": base["training_badge"],
                    "items": TrainingSourceSerializer(sources, many=True, context=self.context).data,
                    "cta": None,
                    "media": {
                        "icon": {
                            "src": self.absolute_media(instance.check_icon),
                            "alt": instance.check_icon_alt,
                        }
                    },
                    "meta": {
                        "rightPill": base["training_right_pill"],
                        "rightTitle": base["training_right_title"],
                        "rightBullets": TrainingRightBulletSerializer(bullets, many=True, context=self.context).data,
                    },
                },
                "summary": {
                    "id": "advantages-summary",
                    "title": base["summary_title"],
                    "subtitle": base["summary_subtitle"],
                    "items": [],
                    "cta": None,
                    "media": {},
                    "meta": {
                        "title": base["summary_title"],
                        "desktopStageLabel": base["desktop_stage_label"],
                        "desktopAiLabel": base["desktop_ai_label"],
                        "desktopHumanLabel": base["desktop_human_label"],
                        "mobileTitle": base["mobile_title"],
                        "mobileSubtitle": base["mobile_subtitle"],
                        "mobileAiLabel": base["mobile_ai_label"],
                        "mobileHumanLabel": base["mobile_human_label"],
                        "mobileFooter": base["mobile_footer"],
                        "desktopFooter": base["summary_description"],
                        "stageDescriptionLabel": base["stage_description_label"],
                    },
                },
                "aiSummary": AiSummarySerializer(ai_summary, many=True, context=self.context).data,
                "humanLimits": HumanLimitSerializer(human_limits, many=True, context=self.context).data,
            },
        }

class AiValueSectionSerializer(MediaUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = AiValueSection
        fields = (
            "title",
            "subtitle_prefix",
            "subtitle_highlight",
            "description",
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
            "integrations_title",
            "integrations_subtitle",
            "integrations_add_aria_label",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        points = instance.value_points.filter(is_active=True).order_by("order", "id")
        integrations = instance.integrations.filter(is_active=True).order_by("order", "id")
        return {
            "id": "ai-value",
            "title": data["title"],
            "subtitle": f"{data['subtitle_prefix']} {data['subtitle_highlight']}".strip(),
            "description": data["description"],
            "items": AiValuePointSerializer(points, many=True, context=self.context).data,
            "cta": None,
            "media": {
                "integrationsBanner": {
                    "src": self.absolute_media(instance.integrations_banner),
                    "alt": instance.integrations_banner_alt,
                }
            },
            "meta": {
                "subtitlePrefix": data["subtitle_prefix"],
                "subtitleHighlight": data["subtitle_highlight"],
                "launch": {
                    "id": "ai-value-launch",
                    "title": data["launch_title"],
                    "description": data["launch_description"],
                    "items": [],
                    "cta": None,
                    "media": {},
                    "meta": {
                        "badgePrimary": data["launch_badge_primary"],
                        "badgeSecondary": data["launch_badge_secondary"],
                        "leftLabel": data["launch_left_label"],
                        "rightLabel": data["launch_right_label"],
                        "paidTitle": data["launch_paid_title"],
                        "paidDescription": data["launch_paid_description"],
                        "noteTitle": data["launch_note_title"],
                        "noteDescription": data["launch_note_description"],
                    },
                },
                "integrations": {
                    "id": "ai-value-integrations",
                    "title": data["integrations_title"],
                    "subtitle": data["integrations_subtitle"],
                    "items": AiIntegrationSerializer(integrations, many=True, context=self.context).data,
                    "cta": None,
                    "media": {
                        "banner": {
                            "src": self.absolute_media(instance.integrations_banner),
                            "alt": instance.integrations_banner_alt,
                        }
                    },
                    "meta": {
                        "addAriaLabel": data["integrations_add_aria_label"],
                    },
                },
            },
        }


class ChannelsSectionSerializer(MediaUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = ChannelsSection
        fields = ("title", "subtitle", "description", "item_aria_label_prefix")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        items = instance.items.filter(is_active=True).order_by("order", "id")
        return {
            "id": "channels",
            "title": data["title"],
            "subtitle": data["subtitle"],
            "description": data["description"],
            "items": ChannelItemSerializer(items, many=True, context=self.context).data,
            "cta": None,
            "media": {
                "background": {
                    "src": self.absolute_media(instance.background_image),
                    "alt": instance.background_alt,
                },
                "image": {
                    "src": self.absolute_media(instance.primary_phone_image),
                    "alt": instance.primary_phone_alt,
                },
                "secondaryImage": {
                    "src": self.absolute_media(instance.secondary_phone_image),
                    "alt": instance.secondary_phone_alt,
                },
            },
            "meta": {
                "itemAriaLabelPrefix": data["item_aria_label_prefix"],
            },
        }


class StepsSectionSerializer(MediaUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = StepsSection
        fields = ("title", "subtitle", "cta_title", "cta_button_label", "cta_button_href")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        steps = instance.steps.filter(is_active=True).order_by("order", "id")
        actions = instance.cta_actions.filter(is_active=True).order_by("order", "id")
        return {
            "id": "steps",
            "title": data["title"],
            "subtitle": data["subtitle"],
            "items": StepItemSerializer(steps, many=True, context=self.context).data,
            "cta": {
                "title": data["cta_title"],
                "titleLines": (data["cta_title"] or "").split("\n"),
                "primary": {
                    "id": "steps-cta-primary",
                    "slug": "steps-cta-primary",
                    "label": data["cta_button_label"],
                    "href": data["cta_button_href"],
                    "sortOrder": 1,
                    "isActive": True,
                },
                "actions": StepCtaActionSerializer(actions, many=True, context=self.context).data,
                "media": {
                    "image": {
                        "src": self.absolute_media(instance.cta_image, fallback=instance.cta_image_source_path),
                        "alt": instance.cta_image_alt,
                    },
                    "background": {
                        "src": self.absolute_media(instance.cta_background_image),
                        "alt": instance.cta_background_alt,
                    },
                },
            },
            "media": {
                "ctaBackground": {
                    "src": self.absolute_media(instance.cta_background_image),
                    "alt": instance.cta_background_alt,
                }
            },
            "meta": {},
        }


class PricingSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingSection
        fields = ("title", "subtitle", "channels_label")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        plans = instance.plans.filter(is_active=True).order_by("order", "id")
        return {
            "id": "pricing",
            "title": data["title"],
            "subtitle": data["subtitle"],
            "items": PricingPlanSerializer(plans, many=True, context=self.context).data,
            "cta": None,
            "media": {},
            "meta": {
                "channelsLabel": data["channels_label"],
            },
        }


class ReviewsSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewsSection
        fields = (
            "title",
            "subtitle",
            "action_read_more",
            "action_close_modal_aria",
            "action_prev_page_aria",
            "action_next_page_aria",
            "action_pagination_aria",
            "action_pagination_go_to",
            "modal_results_title",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        items = instance.items.filter(is_active=True).order_by("order", "id")
        return {
            "id": "reviews",
            "title": data["title"],
            "subtitle": data["subtitle"],
            "items": ReviewItemSerializer(items, many=True, context=self.context).data,
            "cta": None,
            "media": {},
            "meta": {
                "actions": {
                    "readMore": data["action_read_more"],
                    "closeModalAria": data["action_close_modal_aria"],
                    "prevPageAria": data["action_prev_page_aria"],
                    "nextPageAria": data["action_next_page_aria"],
                    "paginationAria": data["action_pagination_aria"],
                    "paginationGoTo": data["action_pagination_go_to"],
                },
                "modalResultsTitle": data["modal_results_title"],
            },
        }


class ContactsSectionSerializer(MediaUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = ContactsSection
        fields = (
            "title",
            "subtitle",
            "description",
            "heading_line3",
            "card_title_line1",
            "card_title_line2",
            "card_response_time",
            "form_title",
            "form_subtitle",
            "form_submit_label",
            "form_close_aria_label",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        messengers = instance.messengers.filter(is_active=True).order_by("order", "id")
        phones = instance.phones.filter(is_active=True).order_by("order", "id")
        emails = instance.emails.filter(is_active=True).order_by("order", "id")
        fields = instance.form_fields.filter(is_active=True).order_by("order", "id")

        channels_section = ChannelsSection.objects.first()
        socials_qs = ChannelItem.objects.none()
        if channels_section:
            socials_qs = channels_section.items.filter(is_active=True).order_by("order", "id")

        messenger_data = ContactMessengerSerializer(messengers, many=True, context=self.context).data
        socials_data = ChannelItemSerializer(socials_qs, many=True, context=self.context).data

        return {
            "id": "contacts",
            "title": data["title"],
            "subtitle": data["subtitle"],
            "description": data["description"],
            "items": messenger_data,
            "cta": None,
            "media": {
                "sectionBackground": {
                    "src": self.absolute_media(instance.section_background_image),
                    "alt": instance.section_background_alt,
                },
                "cardBackground": {
                    "src": self.absolute_media(instance.card_background_image),
                    "alt": instance.card_background_alt,
                },
            },
            "meta": {
                "headingLine3": data["heading_line3"],
                "card": {
                    "titleLine1": data["card_title_line1"],
                    "titleLine2": data["card_title_line2"],
                    "responseTime": data["card_response_time"],
                },
                "form": {
                    "id": "contacts-form",
                    "title": data["form_title"],
                    "subtitle": data["form_subtitle"],
                    "fields": ContactFormFieldSerializer(fields, many=True, context=self.context).data,
                    "submitLabel": data["form_submit_label"],
                    "closeAriaLabel": data["form_close_aria_label"],
                },
            },
            "phones": ContactPhoneSerializer(phones, many=True, context=self.context).data,
            "emails": ContactEmailSerializer(emails, many=True, context=self.context).data,
            "socials": socials_data,
            "messengers": messenger_data,
        }


class FooterSectionSerializer(MediaUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = FooterSection
        fields = ("brand_name", "brand_href", "support_email", "nav_aria_label")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        columns = instance.columns.filter(is_active=True).order_by("order", "id")
        return {
            "id": "footer",
            "items": FooterColumnSerializer(columns, many=True, context=self.context).data,
            "cta": None,
            "media": {
                "logo": {
                    "src": self.absolute_media(instance.logo),
                    "alt": instance.logo_alt or data["brand_name"],
                }
            },
            "meta": {
                "brandName": data["brand_name"],
                "brandHref": data["brand_href"],
                "supportEmail": data["support_email"],
                "navAriaLabel": data["nav_aria_label"],
            },
        }


def serialize_site_data(request) -> dict[str, Any]:
    settings = SiteSettings.objects.first()
    header = HeaderSection.objects.first()
    hero = HeroSection.objects.first()
    hero_logos = HeroLogosSection.objects.first()
    advantages = AdvantagesSection.objects.first()
    ai_value = AiValueSection.objects.first()
    channels = ChannelsSection.objects.first()
    steps = StepsSection.objects.first()
    pricing = PricingSection.objects.first()
    reviews = ReviewsSection.objects.first()
    contacts = ContactsSection.objects.first()
    footer = FooterSection.objects.first()

    context = {"request": request}
    contacts_data = ContactsSectionSerializer(contacts, context=context).data if contacts else {}
    channels_data = ChannelsSectionSerializer(channels, context=context).data if channels else {}

    data = {
        "meta": {
            "brandName": settings.brand_name if settings else "",
            "siteName": (settings.site_name if settings else "") or (settings.brand_name if settings else ""),
            "description": settings.description if settings else "",
            "locale": settings.locale if settings else "ru-RU",
            "theme": settings.theme if settings else "light",
            "supportEmail": settings.support_email if settings else "",
        },
        "events": {
            "contactFormOpen": settings.contact_form_open_event if settings else "contact-feedback-form:open",
        },
        "nav": HeaderSectionSerializer(header, context=context).data if header else {},
        "hero": HeroSectionSerializer(hero, context=context).data if hero else {},
        "heroLogos": HeroLogosSectionSerializer(hero_logos, context=context).data if hero_logos else {},
        "advantages": AdvantagesSectionSerializer(advantages, context=context).data if advantages else {},
        "aiValue": AiValueSectionSerializer(ai_value, context=context).data if ai_value else {},
        "channels": channels_data,
        "steps": StepsSectionSerializer(steps, context=context).data if steps else {},
        "pricing": PricingSectionSerializer(pricing, context=context).data if pricing else {},
        "reviews": ReviewsSectionSerializer(reviews, context=context).data if reviews else {},
        "contacts": contacts_data,
        "footer": FooterSectionSerializer(footer, context=context).data if footer else {},
    }

    logo_src = ""
    logo_alt = ""
    if settings:
        logo_src = HeaderSectionSerializer(context=context).absolute_media(settings.logo)
        logo_alt = settings.logo_alt or settings.brand_name

    hero_src = ""
    hero_alt = ""
    texture_src = ""
    if hero:
        helper = HeroSectionSerializer(context=context)
        hero_src = helper.absolute_media(hero.phone_image)
        hero_alt = hero.phone_alt
        texture_src = helper.absolute_media(hero.texture_image)

    channels_helper = ChannelsSectionSerializer(context=context)
    channels_background = channels_helper.absolute_media(channels.background_image) if channels else ""
    channels_image = channels_helper.absolute_media(channels.primary_phone_image) if channels else ""
    channels_image_alt = channels.primary_phone_alt if channels else ""
    channels_secondary = channels_helper.absolute_media(channels.secondary_phone_image) if channels else ""

    steps_helper = StepsSectionSerializer(context=context)
    cta_bg = steps_helper.absolute_media(steps.cta_background_image) if steps else ""
    cta_image = steps_helper.absolute_media(steps.cta_image, fallback=steps.cta_image_source_path) if steps else ""

    check_icon = ""
    if advantages:
        check_icon = AdvantagesSectionSerializer(context=context).absolute_media(advantages.check_icon)

    hero_logos_items = data.get("heroLogos", {}).get("items", [])
    social_items = channels_data.get("items", []) if channels_data else []
    steps_items = data.get("steps", {}).get("items", [])

    def step_media(index: int) -> tuple[str, str]:
        if len(steps_items) > index:
            image = steps_items[index].get("media", {}).get("image", {})
            return image.get("src", ""), image.get("alt", "")
        return "", ""

    step_day1_src, step_day1_alt = step_media(0)
    step_day2_src, step_day2_alt = step_media(1)
    step_day3_src, step_day3_alt = step_media(2)
    step_day4_src, step_day4_alt = step_media(3)
    step_month_src, step_month_alt = step_media(4)

    asset_items = [
        {"id": "asset-logo", "slug": "logo", "src": logo_src, "alt": logo_alt, "sortOrder": 1, "isActive": True},
        {"id": "asset-hero-phone", "slug": "hero-phone", "src": hero_src, "alt": hero_alt, "sortOrder": 2, "isActive": True},
        {"id": "asset-hero-texture", "slug": "hero-texture", "src": texture_src, "alt": "", "sortOrder": 3, "isActive": True},
        {"id": "asset-social-phone", "slug": "social-phone", "src": channels_image, "alt": channels_image_alt, "sortOrder": 4, "isActive": True},
        {"id": "asset-social-phone-secondary", "slug": "social-phone-secondary", "src": channels_secondary, "alt": channels_image_alt, "sortOrder": 5, "isActive": True},
        {"id": "asset-section-background", "slug": "section-background", "src": channels_background, "alt": "", "sortOrder": 6, "isActive": True},
        {"id": "asset-cta-background", "slug": "cta-background", "src": cta_bg, "alt": "", "sortOrder": 7, "isActive": True},
        {"id": "asset-integrations-banner", "slug": "integrations-banner", "src": data.get("aiValue", {}).get("media", {}).get("integrationsBanner", {}).get("src", ""), "alt": "", "sortOrder": 8, "isActive": True},
        {"id": "asset-integrations-step-day1", "slug": "integrations-step-day1", "src": step_day1_src, "alt": step_day1_alt, "sortOrder": 9, "isActive": True},
        {"id": "asset-integrations-step-day2", "slug": "integrations-step-day2", "src": step_day2_src, "alt": step_day2_alt, "sortOrder": 10, "isActive": True},
        {"id": "asset-integrations-step-day3", "slug": "integrations-step-day3", "src": step_day3_src, "alt": step_day3_alt, "sortOrder": 11, "isActive": True},
        {"id": "asset-integrations-step-day4", "slug": "integrations-step-day4", "src": step_day4_src, "alt": step_day4_alt, "sortOrder": 12, "isActive": True},
        {"id": "asset-integrations-step-monthly", "slug": "integrations-step-monthly", "src": step_month_src, "alt": step_month_alt, "sortOrder": 13, "isActive": True},
        {"id": "asset-check", "slug": "check", "src": check_icon, "alt": "", "sortOrder": 14, "isActive": True},
    ]

    for index, item in enumerate(hero_logos_items, start=10):
        asset_items.append(
            {
                "id": f"asset-hero-logo-{index - 9}",
                "slug": f"hero-logo-{index - 9}",
                "src": item.get("src", ""),
                "alt": item.get("alt", ""),
                "sortOrder": index,
                "isActive": True,
            }
        )

    for index, item in enumerate(social_items, start=len(asset_items) + 1):
        asset_items.append(
            {
                "id": f"asset-social-icon-{item.get('slug', index)}",
                "slug": f"social-icon-{item.get('slug', index)}",
                "src": item.get("icon", {}).get("src", ""),
                "alt": item.get("icon", {}).get("alt", ""),
                "sortOrder": index,
                "isActive": True,
            }
        )

    data["assets"] = {
        "id": "assets",
        "title": "Asset Registry",
        "description": "Реестр медиа, которые используются в лендинге.",
        "items": asset_items,
        "cta": None,
        "media": {
            "logo": {"src": logo_src, "alt": logo_alt},
            "heroPhone": {"src": hero_src, "alt": hero_alt},
            "heroTexture": {"src": texture_src, "alt": ""},
            "socialPhone": {"src": channels_image, "alt": channels_image_alt},
            "socialPhoneSecondary": {"src": channels_secondary, "alt": channels_image_alt},
            "sectionBackground": {"src": channels_background, "alt": ""},
            "ctaBackground": {"src": cta_bg, "alt": ""},
            "integrationsBanner": {
                "src": data.get("aiValue", {}).get("media", {}).get("integrationsBanner", {}).get("src", ""),
                "alt": "",
            },
            "integrationsStepDay1": {"src": step_day1_src, "alt": step_day1_alt},
            "integrationsStepDay2": {"src": step_day2_src, "alt": step_day2_alt},
            "integrationsStepDay3": {"src": step_day3_src, "alt": step_day3_alt},
            "integrationsStepDay4": {"src": step_day4_src, "alt": step_day4_alt},
            "integrationsStepMonthly": {"src": step_month_src, "alt": step_month_alt},
            "integrationsCtaImage": {"src": cta_image, "alt": ""},
            "checkIcon": {"src": check_icon, "alt": ""},
        },
        "meta": {},
    }

    return data
