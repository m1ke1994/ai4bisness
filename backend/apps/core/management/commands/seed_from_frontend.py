import html
import json
import os
import re
import subprocess
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

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
from apps.core.services import MediaImporter


class Command(BaseCommand):
    help = "Импортирует контент и медиа из nuxt-app/data/siteData.ts в CMS"

    def add_arguments(self, parser):
        parser.add_argument("--if-empty", action="store_true", help="Запускать только если CMS ещё не заполнена")

    def handle(self, *args, **options):
        self.report = {
            "created": 0,
            "updated": 0,
            "images_imported": 0,
            "images_reused": 0,
            "images_missing": 0,
        }
        self.missing_media = set()

        if options["if_empty"] and SiteSettings.objects.exists():
            self._log_warn("Сидинг пропущен: данные уже существуют.")
            return

        self.backend_root = Path(__file__).resolve().parents[4]
        self.project_root = self.backend_root.parent
        frontend_dir_env = os.getenv("FRONTEND_DIR", "").strip()
        self.frontend_dir = (Path(frontend_dir_env) if frontend_dir_env else self.project_root / "nuxt-app").resolve()
        self.tmp_dir = self.backend_root / "tmp"
        self.site_data_json = self.tmp_dir / "siteData.json"
        self.site_data_source = self.frontend_dir / "data" / "siteData.ts"
        self.export_script = self.backend_root / "scripts" / "export_site_data.mjs"

        if not self.frontend_dir.exists():
            raise CommandError(f"Не найдена папка фронтенда: {self.frontend_dir}")
        if not self.export_script.exists():
            raise CommandError(f"Не найден node-экспортер: {self.export_script}")

        self.media_importer = MediaImporter(frontend_dir=self.frontend_dir)
        self._log_info(f"Фронтенд: {self.frontend_dir}")
        self._log_info(f"JSON контента: {self.site_data_json}")

        payload = self._load_frontend_payload()
        site_data = payload.get("siteData") or {}
        legacy_data = payload.get("legacyData") or {}

        with transaction.atomic():
            self._seed_site_settings(site_data)
            self._seed_header(site_data)
            self._seed_hero(site_data)
            self._seed_hero_logos(site_data)
            self._seed_advantages(site_data, legacy_data)
            self._seed_ai_value(site_data, legacy_data)
            self._seed_channels(site_data)
            self._seed_steps(site_data)
            self._seed_pricing(site_data)
            self._seed_reviews(site_data)
            self._seed_contacts(site_data)
            self._seed_footer(site_data)
            self._seed_policy_pages()

        self.report["images_missing"] = len(self.missing_media)

        self._log_ok("Сидинг завершён.")
        self._log_info(
            "summary: "
            f"created={self.report['created']}, "
            f"updated={self.report['updated']}, "
            f"images_imported={self.report['images_imported']}, "
            f"images_reused={self.report['images_reused']}, "
            f"images_missing={self.report['images_missing']}"
        )

        if self.missing_media:
            self._log_warn("Отсутствующие файлы:")
            for path in sorted(self.missing_media):
                self._log_warn(path)

    def _log_info(self, message: str):
        self.stdout.write(f"[INFO] {message}")

    def _log_ok(self, message: str):
        self.stdout.write(self.style.SUCCESS(f"[OK] {message}"))

    def _log_warn(self, message: str):
        self.stdout.write(self.style.WARNING(f"[WARN] {message}"))

    def _load_frontend_payload(self) -> dict:
        if not self.site_data_source.exists():
            raise CommandError(f"Не найден файл контента: {self.site_data_source}")

        self._ensure_site_data_json()

        if not self.site_data_json.exists():
            raise CommandError(f"Не найден JSON контента после экспорта: {self.site_data_json}")

        try:
            with self.site_data_json.open("r", encoding="utf-8") as source_handle:
                payload = json.load(source_handle)
        except json.JSONDecodeError as exc:
            raise CommandError(f"Не удалось распарсить JSON: {self.site_data_json}") from exc

        if not isinstance(payload, dict):
            raise CommandError("Некорректный формат payload: ожидается JSON-объект.")
        return payload

    def _ensure_site_data_json(self):
        needs_export = not self.site_data_json.exists()
        if not needs_export:
            try:
                source_mtime = self.site_data_source.stat().st_mtime
                json_mtime = self.site_data_json.stat().st_mtime
                needs_export = source_mtime > json_mtime
            except OSError:
                needs_export = True

        if needs_export:
            self._run_exporter()
        else:
            self._log_info("Используется существующий backend/tmp/siteData.json")

    def _run_exporter(self):
        env = os.environ.copy()
        env["FRONTEND_DIR"] = str(self.frontend_dir)
        env["SITE_DATA_JSON"] = str(self.site_data_json)
        env["SITE_DATA_SOURCE"] = str(self.site_data_source)

        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        self._log_info("Запуск node-экспортера siteData.ts -> JSON")

        try:
            result = subprocess.run(
                ["node", str(self.export_script)],
                check=True,
                capture_output=True,
                text=True,
                env=env,
            )
        except FileNotFoundError as exc:
            raise CommandError("Node.js не найден. Для seed_from_frontend нужен node.") from exc
        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or "").strip()
            raise CommandError(f"Ошибка выполнения export_site_data.mjs: {stderr}") from exc

        stdout = (result.stdout or "").strip()
        if stdout:
            for line in stdout.splitlines():
                if line.startswith("["):
                    self.stdout.write(line)
                else:
                    self._log_info(line)

    def _clean_text(self, value):
        if value is None:
            return ""
        return str(value).strip()

    def _to_slug(self, raw: str, prefix: str, index: int) -> str:
        base = slugify(self._clean_text(raw), allow_unicode=True)
        if base:
            return base
        return f"{prefix}-{index}"

    def _set_image(self, instance, field_name: str, src: str, upload_dir: str):
        src = self._clean_text(src)
        image_field = getattr(instance, field_name)

        if not src:
            if image_field and image_field.name:
                image_field.delete(save=False)
            return

        result = self.media_importer.import_image(src, upload_dir)
        if result.status == MediaImporter.STATUS_MISSING or not result.storage_name:
            self.missing_media.add(src)
            self._log_warn(f"missing media [{instance._meta.model_name}.{field_name}]: {src}")
            return

        if image_field.name != result.storage_name:
            image_field.name = result.storage_name

        if result.status == MediaImporter.STATUS_IMPORTED:
            self.report["images_imported"] += 1
        else:
            self.report["images_reused"] += 1

    def _upsert(self, model, defaults: dict, **lookup):
        obj, created = model.objects.update_or_create(defaults=defaults, **lookup)
        if created:
            self.report["created"] += 1
        else:
            self.report["updated"] += 1
        return obj

    def _seed_site_settings(self, site_data: dict):
        meta = site_data.get("meta", {})
        events = site_data.get("events", {})
        assets_media = site_data.get("assets", {}).get("media", {})

        settings = self._upsert(
            SiteSettings,
            singleton_key=1,
            defaults={
                "brand_name": self._clean_text(meta.get("brandName")),
                "site_name": self._clean_text(meta.get("siteName")),
                "description": self._clean_text(meta.get("description")),
                "locale": self._clean_text(meta.get("locale")) or "ru-RU",
                "theme": self._clean_text(meta.get("theme")) or "light",
                "support_email": self._clean_text(meta.get("supportEmail")),
                "contact_form_open_event": self._clean_text(events.get("contactFormOpen")) or "contact-feedback-form:open",
            },
        )

        logo_data = assets_media.get("logo", {})
        settings.logo_alt = self._clean_text(logo_data.get("alt")) or settings.brand_name
        self._set_image(settings, "logo", self._clean_text(logo_data.get("src")), "site")

        favicon_data = assets_media.get("favicon", {})
        self._set_image(settings, "favicon", self._clean_text(favicon_data.get("src")), "site")
        settings.save()

    def _seed_header(self, site_data: dict):
        nav = site_data.get("nav", {})
        meta = nav.get("meta", {})
        aria = meta.get("aria", {})

        section = self._upsert(
            HeaderSection,
            singleton_key=1,
            defaults={
                "is_active": True,
                "brand_href": self._clean_text(meta.get("brandHref")) or "/",
                "aria_desktop_nav": self._clean_text(aria.get("desktopNav")),
                "aria_mobile_nav": self._clean_text(aria.get("mobileNav")),
                "aria_mobile_dialog": self._clean_text(aria.get("mobileDialog")),
                "aria_open_menu": self._clean_text(aria.get("openMenu")),
                "aria_close_menu": self._clean_text(aria.get("closeMenu")),
            },
        )

        seen_nav_slugs = []
        for index, item in enumerate(nav.get("items", []), start=1):
            slug = self._clean_text(item.get("slug")) or self._to_slug(item.get("label"), "nav", index)
            seen_nav_slugs.append(slug)
            self._upsert(
                HeaderNavItem,
                section=section,
                slug=slug,
                defaults={
                    "label": self._clean_text(item.get("label")),
                    "href": self._clean_text(item.get("href")),
                    "order": int(item.get("sortOrder") or index),
                    "is_active": bool(item.get("isActive", True)),
                    "is_external": str(item.get("href", "")).startswith("http"),
                },
            )
        HeaderNavItem.objects.filter(section=section).exclude(slug__in=seen_nav_slugs).update(is_active=False)

        seen_mobile_slugs = []
        for index, item in enumerate(meta.get("mobileSocials", []), start=1):
            slug = self._clean_text(item.get("slug")) or self._to_slug(item.get("label"), "mobile-social", index)
            seen_mobile_slugs.append(slug)
            obj = self._upsert(
                HeaderMobileSocialItem,
                section=section,
                slug=slug,
                defaults={
                    "label": self._clean_text(item.get("label")),
                    "href": self._clean_text(item.get("href")),
                    "aria_label": self._clean_text(item.get("ariaLabel")) or self._clean_text(item.get("label")),
                    "icon_alt": self._clean_text(item.get("icon", {}).get("alt")) or self._clean_text(item.get("label")),
                    "order": int(item.get("sortOrder") or index),
                    "is_active": bool(item.get("isActive", True)),
                    "is_external": str(item.get("href", "")).startswith("http"),
                },
            )
            self._set_image(obj, "icon", self._clean_text(item.get("icon", {}).get("src")), "header/mobile_social")
            obj.save()
        HeaderMobileSocialItem.objects.filter(section=section).exclude(slug__in=seen_mobile_slugs).update(is_active=False)

    def _seed_hero(self, site_data: dict):
        hero = site_data.get("hero", {})
        section = self._upsert(
            HeroSection,
            singleton_key=1,
            defaults={
                "is_active": True,
                "title": self._clean_text(hero.get("title")),
                "subtitle": self._clean_text(hero.get("subtitle")),
                "description": self._clean_text(hero.get("description")),
                "stats_disclaimer": self._clean_text(hero.get("meta", {}).get("statsDisclaimer")),
                "phone_alt": self._clean_text(hero.get("media", {}).get("image", {}).get("alt")),
                "texture_alt": self._clean_text(hero.get("media", {}).get("texture", {}).get("alt")),
                "image_vars": hero.get("meta", {}).get("imageVars") or {},
            },
        )
        self._set_image(section, "phone_image", self._clean_text(hero.get("media", {}).get("image", {}).get("src")), "hero")
        self._set_image(section, "texture_image", self._clean_text(hero.get("media", {}).get("texture", {}).get("src")), "hero")
        section.save()

        seen_stats = []
        for index, item in enumerate(hero.get("items", []), start=1):
            slug = self._clean_text(item.get("slug")) or f"hero-stat-{index}"
            seen_stats.append(slug)
            self._upsert(
                HeroStatItem,
                section=section,
                slug=slug,
                defaults={
                    "value": self._clean_text(item.get("value")),
                    "text": self._clean_text(item.get("text")),
                    "order": int(item.get("sortOrder") or index),
                    "is_active": bool(item.get("isActive", True)),
                },
            )
        HeroStatItem.objects.filter(section=section).exclude(slug__in=seen_stats).update(is_active=False)

    def _seed_hero_logos(self, site_data: dict):
        section = self._upsert(HeroLogosSection, singleton_key=1, defaults={"is_active": True})
        seen = []
        for index, item in enumerate(site_data.get("heroLogos", {}).get("items", []), start=1):
            slug = self._clean_text(item.get("slug")) or f"hero-logo-{index}"
            seen.append(slug)
            obj = self._upsert(
                HeroLogoItem,
                section=section,
                slug=slug,
                defaults={
                    "logo_alt": self._clean_text(item.get("alt")),
                    "source_path": self._clean_text(item.get("src")),
                    "order": int(item.get("sortOrder") or index),
                    "is_active": bool(item.get("isActive", True)),
                },
            )
            self._set_image(obj, "logo", self._clean_text(item.get("src")), "hero/logos")
            obj.source_path = self._clean_text(item.get("src"))
            obj.save()
        HeroLogoItem.objects.filter(section=section).exclude(slug__in=seen).update(is_active=False)

    def _seed_advantages(self, site_data: dict, legacy_data: dict):
        advantages = site_data.get("advantages", {})
        meta_training = advantages.get("meta", {}).get("training", {})
        meta_summary = advantages.get("meta", {}).get("summary", {}).get("meta", {})

        section = self._upsert(
            AdvantagesSection,
            singleton_key=1,
            defaults={
                "is_active": True,
                "training_badge": self._clean_text(meta_training.get("title") or advantages.get("title")),
                "training_right_pill": self._clean_text(meta_training.get("meta", {}).get("rightPill")),
                "training_right_title": self._clean_text(meta_training.get("meta", {}).get("rightTitle")),
                "summary_title": self._clean_text(meta_summary.get("title") or advantages.get("subtitle")),
                "summary_subtitle": self._clean_text(advantages.get("meta", {}).get("summary", {}).get("subtitle")),
                "summary_description": self._clean_text(meta_summary.get("desktopFooter") or advantages.get("description")),
                "desktop_stage_label": self._clean_text(meta_summary.get("desktopStageLabel")),
                "desktop_ai_label": self._clean_text(meta_summary.get("desktopAiLabel")),
                "desktop_human_label": self._clean_text(meta_summary.get("desktopHumanLabel")),
                "mobile_title": self._clean_text(meta_summary.get("mobileTitle")),
                "mobile_subtitle": self._clean_text(meta_summary.get("mobileSubtitle")),
                "mobile_ai_label": self._clean_text(meta_summary.get("mobileAiLabel")),
                "mobile_human_label": self._clean_text(meta_summary.get("mobileHumanLabel")),
                "mobile_footer": self._clean_text(meta_summary.get("mobileFooter")),
                "stage_description_label": self._clean_text(meta_summary.get("stageDescriptionLabel")),
                "check_icon_alt": self._clean_text(advantages.get("media", {}).get("icon", {}).get("alt")),
            },
        )
        self._set_image(section, "check_icon", self._clean_text(advantages.get("media", {}).get("icon", {}).get("src")), "advantages")
        section.save()

        legacy_stats = legacy_data.get("whatSellerCan", {}).get("stats", [])
        seen_stats = []
        for index, item in enumerate(legacy_stats, start=1):
            slug = f"adv-stat-{index}"
            seen_stats.append(slug)
            self._upsert(
                AdvantagesStatItem,
                section=section,
                slug=slug,
                defaults={
                    "value": self._clean_text(item.get("value")),
                    "text": self._clean_text(item.get("text")),
                    "order": index,
                    "is_active": True,
                },
            )
        AdvantagesStatItem.objects.filter(section=section).exclude(slug__in=seen_stats).update(is_active=False)

        self._seed_text_items(section.training_sources, TrainingSourceItem, section, meta_training.get("items", []), value_field="title")
        self._seed_text_items(section.training_right_bullets, TrainingRightBulletItem, section, meta_training.get("meta", {}).get("rightBullets", []))

        rows_seen = []
        for index, item in enumerate(advantages.get("items", []), start=1):
            slug = self._clean_text(item.get("slug")) or f"comparison-{index}"
            rows_seen.append(slug)
            self._upsert(
                ComparisonRowItem,
                section=section,
                slug=slug,
                defaults={
                    "title": self._clean_text(item.get("title")),
                    "ai_description": self._clean_text(item.get("aiDescription")),
                    "human_description": self._clean_text(item.get("humanDescription")),
                    "order": int(item.get("sortOrder") or index),
                    "is_active": bool(item.get("isActive", True)),
                },
            )
        ComparisonRowItem.objects.filter(section=section).exclude(slug__in=rows_seen).update(is_active=False)

        self._seed_text_items(section.ai_summary_items, AdvantagesAiSummaryItem, section, advantages.get("meta", {}).get("aiSummary", []))
        self._seed_text_items(section.human_limit_items, AdvantagesHumanLimitItem, section, advantages.get("meta", {}).get("humanLimits", []))

    def _seed_ai_value(self, site_data: dict, legacy_data: dict):
        ai_value = site_data.get("aiValue", {})
        launch_meta = ai_value.get("meta", {}).get("launch", {}).get("meta", {})
        integrations_meta = ai_value.get("meta", {}).get("integrations", {})

        section = self._upsert(
            AiValueSection,
            singleton_key=1,
            defaults={
                "is_active": True,
                "title": self._clean_text(ai_value.get("title")),
                "subtitle_prefix": self._clean_text(ai_value.get("meta", {}).get("subtitlePrefix")),
                "subtitle_highlight": self._clean_text(ai_value.get("meta", {}).get("subtitleHighlight")),
                "description": self._clean_text(ai_value.get("description")),
                "launch_badge_primary": self._clean_text(launch_meta.get("badgePrimary")),
                "launch_badge_secondary": self._clean_text(launch_meta.get("badgeSecondary")),
                "launch_title": self._clean_text(ai_value.get("meta", {}).get("launch", {}).get("title"))
                or self._clean_text(legacy_data.get("aiValue", {}).get("launch", {}).get("title")),
                "launch_description": self._clean_text(ai_value.get("meta", {}).get("launch", {}).get("description")),
                "launch_left_label": self._clean_text(launch_meta.get("leftLabel")),
                "launch_right_label": self._clean_text(launch_meta.get("rightLabel")),
                "launch_paid_title": self._clean_text(launch_meta.get("paidTitle")),
                "launch_paid_description": self._clean_text(launch_meta.get("paidDescription")),
                "launch_note_title": self._clean_text(launch_meta.get("noteTitle"))
                or self._clean_text(legacy_data.get("aiValue", {}).get("launch", {}).get("noteTitle")),
                "launch_note_description": self._clean_text(launch_meta.get("noteDescription")),
                "integrations_title": self._clean_text(integrations_meta.get("title")),
                "integrations_subtitle": self._clean_text(integrations_meta.get("subtitle")),
                "integrations_add_aria_label": self._clean_text(integrations_meta.get("meta", {}).get("addAriaLabel")),
                "integrations_banner_alt": self._clean_text(ai_value.get("media", {}).get("integrationsBanner", {}).get("alt")),
            },
        )
        self._set_image(section, "integrations_banner", self._clean_text(ai_value.get("media", {}).get("integrationsBanner", {}).get("src")), "ai_value")
        section.save()

        self._seed_text_items(section.value_points, AiValuePointItem, section, ai_value.get("items", []))

        seen = []
        for index, item in enumerate(integrations_meta.get("items", []), start=1):
            slug = self._clean_text(item.get("slug")) or f"integration-{index}"
            seen.append(slug)
            obj = self._upsert(
                AiIntegrationItem,
                section=section,
                slug=slug,
                defaults={
                    "title": self._clean_text(item.get("title")),
                    "description": self._clean_text(item.get("description")),
                    "image_alt": self._clean_text(item.get("media", {}).get("image", {}).get("alt")),
                    "source_path": self._clean_text(item.get("media", {}).get("image", {}).get("src")),
                    "order": int(item.get("sortOrder") or index),
                    "is_active": bool(item.get("isActive", True)),
                },
            )
            self._set_image(obj, "image", self._clean_text(item.get("media", {}).get("image", {}).get("src")), "ai_value/integrations")
            obj.source_path = self._clean_text(item.get("media", {}).get("image", {}).get("src"))
            obj.save()
        AiIntegrationItem.objects.filter(section=section).exclude(slug__in=seen).update(is_active=False)

    def _seed_channels(self, site_data: dict):
        channels = site_data.get("channels", {})
        section = self._upsert(
            ChannelsSection,
            singleton_key=1,
            defaults={
                "is_active": True,
                "title": self._clean_text(channels.get("title")),
                "subtitle": self._clean_text(channels.get("subtitle")),
                "description": self._clean_text(channels.get("description")),
                "item_aria_label_prefix": self._clean_text(channels.get("meta", {}).get("itemAriaLabelPrefix")),
                "background_alt": self._clean_text(channels.get("media", {}).get("background", {}).get("alt")),
                "primary_phone_alt": self._clean_text(channels.get("media", {}).get("image", {}).get("alt")),
                "secondary_phone_alt": self._clean_text(channels.get("media", {}).get("secondaryImage", {}).get("alt")),
            },
        )
        self._set_image(section, "background_image", self._clean_text(channels.get("media", {}).get("background", {}).get("src")), "channels")
        self._set_image(section, "primary_phone_image", self._clean_text(channels.get("media", {}).get("image", {}).get("src")), "channels")
        self._set_image(section, "secondary_phone_image", self._clean_text(channels.get("media", {}).get("secondaryImage", {}).get("src")), "channels")
        section.save()

        seen = []
        for index, item in enumerate(channels.get("items", []), start=1):
            slug = self._clean_text(item.get("slug")) or f"channel-{index}"
            seen.append(slug)
            obj = self._upsert(
                ChannelItem,
                section=section,
                slug=slug,
                defaults={
                    "name": self._clean_text(item.get("name")),
                    "href": self._clean_text(item.get("href")),
                    "icon_alt": self._clean_text(item.get("icon", {}).get("alt")) or self._clean_text(item.get("name")),
                    "order": int(item.get("sortOrder") or index),
                    "is_active": bool(item.get("isActive", True)),
                    "is_external": str(item.get("href", "")).startswith("http"),
                },
            )
            self._set_image(obj, "icon", self._clean_text(item.get("icon", {}).get("src")), "channels/icons")
            obj.save()
        ChannelItem.objects.filter(section=section).exclude(slug__in=seen).update(is_active=False)

    def _seed_steps(self, site_data: dict):
        steps = site_data.get("steps", {})
        cta = steps.get("cta", {})

        section = self._upsert(
            StepsSection,
            singleton_key=1,
            defaults={
                "is_active": True,
                "title": self._clean_text(steps.get("title")),
                "subtitle": self._clean_text(steps.get("subtitle")),
                "cta_title": self._clean_text(cta.get("title")),
                "cta_button_label": self._clean_text(cta.get("primary", {}).get("label")),
                "cta_button_href": self._clean_text(cta.get("primary", {}).get("href")) or "#contacts",
                "cta_image_alt": self._clean_text(cta.get("media", {}).get("image", {}).get("alt")),
                "cta_image_source_path": self._clean_text(cta.get("media", {}).get("image", {}).get("src")),
                "cta_background_alt": self._clean_text(cta.get("media", {}).get("background", {}).get("alt")),
            },
        )
        self._set_image(section, "cta_image", self._clean_text(cta.get("media", {}).get("image", {}).get("src")), "steps")
        self._set_image(section, "cta_background_image", self._clean_text(cta.get("media", {}).get("background", {}).get("src")), "steps")
        section.save()

        seen_steps = []
        for index, item in enumerate(steps.get("items", []), start=1):
            slug = self._clean_text(item.get("slug")) or f"step-{index}"
            seen_steps.append(slug)
            obj = self._upsert(
                StepItem,
                section=section,
                slug=slug,
                defaults={
                    "day": self._clean_text(item.get("day")),
                    "title": self._clean_text(item.get("title")),
                    "description": self._clean_text(item.get("description")),
                    "image_alt": self._clean_text(item.get("media", {}).get("image", {}).get("alt")),
                    "source_path": self._clean_text(item.get("media", {}).get("image", {}).get("src")),
                    "order": int(item.get("sortOrder") or index),
                    "is_active": bool(item.get("isActive", True)),
                },
            )
            self._set_image(obj, "image", self._clean_text(item.get("media", {}).get("image", {}).get("src")), "steps/items")
            obj.source_path = self._clean_text(item.get("media", {}).get("image", {}).get("src"))
            obj.save()
        StepItem.objects.filter(section=section).exclude(slug__in=seen_steps).update(is_active=False)

        seen_actions = []
        for index, item in enumerate(cta.get("actions", []), start=1):
            slug = self._clean_text(item.get("slug")) or f"step-cta-{index}"
            seen_actions.append(slug)
            self._upsert(
                StepCtaActionItem,
                section=section,
                slug=slug,
                defaults={
                    "label": self._clean_text(item.get("label")),
                    "href": self._clean_text(item.get("href")),
                    "aria_label": self._clean_text(item.get("ariaLabel")),
                    "order": int(item.get("sortOrder") or index),
                    "is_active": bool(item.get("isActive", True)),
                    "is_external": str(item.get("href", "")).startswith("http"),
                },
            )
        StepCtaActionItem.objects.filter(section=section).exclude(slug__in=seen_actions).update(is_active=False)

    def _seed_pricing(self, site_data: dict):
        pricing = site_data.get("pricing", {})
        section = self._upsert(
            PricingSection,
            singleton_key=1,
            defaults={
                "is_active": True,
                "title": self._clean_text(pricing.get("title")),
                "subtitle": self._clean_text(pricing.get("subtitle")),
                "channels_label": self._clean_text(pricing.get("meta", {}).get("channelsLabel")) or "Каналы:",
            },
        )

        seen_plans = []
        for index, item in enumerate(pricing.get("items", []), start=1):
            slug = self._clean_text(item.get("slug")) or f"plan-{index}"
            seen_plans.append(slug)
            plan = self._upsert(
                PricingPlan,
                section=section,
                slug=slug,
                defaults={
                    "title": self._clean_text(item.get("title")),
                    "subtitle": self._clean_text(item.get("subtitle")),
                    "channels": self._clean_text(item.get("channels")),
                    "accent_badge": self._clean_text(item.get("accentBadge")),
                    "inherit_line": self._clean_text(item.get("inheritLine")),
                    "featured": bool(item.get("meta", {}).get("featured", False)),
                    "dark_card": bool(item.get("meta", {}).get("darkCard", False)),
                    "cta_label": self._clean_text(item.get("cta", {}).get("label")),
                    "cta_href": self._clean_text(item.get("cta", {}).get("href")) or "#contacts",
                    "order": int(item.get("sortOrder") or index),
                    "is_active": bool(item.get("isActive", True)),
                },
            )

            self._seed_text_items(plan.features, PricingPlanFeature, plan, item.get("features", []))
        PricingPlan.objects.filter(section=section).exclude(slug__in=seen_plans).update(is_active=False)

    def _seed_reviews(self, site_data: dict):
        reviews = site_data.get("reviews", {})
        actions = reviews.get("meta", {}).get("actions", {})

        section = self._upsert(
            ReviewsSection,
            singleton_key=1,
            defaults={
                "is_active": True,
                "title": self._clean_text(reviews.get("title")),
                "subtitle": self._clean_text(reviews.get("subtitle")),
                "action_read_more": self._clean_text(actions.get("readMore")),
                "action_close_modal_aria": self._clean_text(actions.get("closeModalAria")),
                "action_prev_page_aria": self._clean_text(actions.get("prevPageAria")),
                "action_next_page_aria": self._clean_text(actions.get("nextPageAria")),
                "action_pagination_aria": self._clean_text(actions.get("paginationAria")),
                "action_pagination_go_to": self._clean_text(actions.get("paginationGoTo")),
                "modal_results_title": self._clean_text(reviews.get("meta", {}).get("modalResultsTitle")),
            },
        )

        seen_reviews = []
        for index, item in enumerate(reviews.get("items", []), start=1):
            slug = self._clean_text(item.get("slug")) or f"review-{index}"
            seen_reviews.append(slug)
            review = self._upsert(
                ReviewItem,
                section=section,
                slug=slug,
                defaults={
                    "company": self._clean_text(item.get("company")),
                    "person": self._clean_text(item.get("person")),
                    "rating": item.get("meta", {}).get("rating"),
                    "order": int(item.get("sortOrder") or index),
                    "is_active": bool(item.get("isActive", True)),
                },
            )

            self._seed_text_items(review.preview_paragraphs, ReviewPreviewParagraph, review, item.get("previewParagraphs", []))
            self._seed_text_items(review.preview_bullets, ReviewPreviewBullet, review, item.get("previewBullets", []))
            self._seed_text_items(review.detail_paragraphs, ReviewDetailParagraph, review, item.get("detailsParagraphs", []))
            self._seed_text_items(review.results, ReviewResultItem, review, item.get("results", []))

        ReviewItem.objects.filter(section=section).exclude(slug__in=seen_reviews).update(is_active=False)

    def _seed_contacts(self, site_data: dict):
        contacts = site_data.get("contacts", {})
        meta = contacts.get("meta", {})
        card = meta.get("card", {})
        form = meta.get("form", {})

        section = self._upsert(
            ContactsSection,
            singleton_key=1,
            defaults={
                "is_active": True,
                "title": self._clean_text(contacts.get("title")),
                "subtitle": self._clean_text(contacts.get("subtitle")),
                "heading_line3": self._clean_text(meta.get("headingLine3")),
                "description": self._clean_text(contacts.get("description")),
                "card_title_line1": self._clean_text(card.get("titleLine1")),
                "card_title_line2": self._clean_text(card.get("titleLine2")),
                "card_response_time": self._clean_text(card.get("responseTime")),
                "form_title": self._clean_text(form.get("title")),
                "form_subtitle": self._clean_text(form.get("subtitle")),
                "form_submit_label": self._clean_text(form.get("submitLabel")),
                "form_close_aria_label": self._clean_text(form.get("closeAriaLabel")),
                "section_background_alt": self._clean_text(contacts.get("media", {}).get("sectionBackground", {}).get("alt")),
                "card_background_alt": self._clean_text(contacts.get("media", {}).get("cardBackground", {}).get("alt")),
            },
        )
        self._set_image(section, "section_background_image", self._clean_text(contacts.get("media", {}).get("sectionBackground", {}).get("src")), "contacts")
        self._set_image(section, "card_background_image", self._clean_text(contacts.get("media", {}).get("cardBackground", {}).get("src")), "contacts")
        section.save()

        seen_messengers = []
        for index, item in enumerate(contacts.get("messengers", contacts.get("items", [])), start=1):
            slug = self._clean_text(item.get("slug")) or f"messenger-{index}"
            seen_messengers.append(slug)
            obj = self._upsert(
                ContactMessenger,
                section=section,
                slug=slug,
                defaults={
                    "name": self._clean_text(item.get("name")),
                    "label": self._clean_text(item.get("label")),
                    "href": self._clean_text(item.get("href")),
                    "icon_alt": self._clean_text(item.get("icon", {}).get("alt")) or self._clean_text(item.get("label")),
                    "aria_label": self._clean_text(item.get("ariaLabel")),
                    "message": self._clean_text(item.get("message")),
                    "order": int(item.get("sortOrder") or index),
                    "is_active": bool(item.get("isActive", True)),
                    "is_external": str(item.get("href", "")).startswith("http"),
                },
            )
            self._set_image(obj, "icon", self._clean_text(item.get("icon", {}).get("src")), "contacts/messengers")
            obj.save()
        ContactMessenger.objects.filter(section=section).exclude(slug__in=seen_messengers).update(is_active=False)

        seen_fields = []
        for index, item in enumerate(form.get("fields", []), start=1):
            slug = self._clean_text(item.get("slug")) or f"form-field-{index}"
            seen_fields.append(slug)
            self._upsert(
                ContactFormField,
                section=section,
                slug=slug,
                defaults={
                    "field_key": self._clean_text(item.get("key")),
                    "label": self._clean_text(item.get("label")),
                    "placeholder": self._clean_text(item.get("placeholder")),
                    "field_type": self._clean_text(item.get("type")) or "text",
                    "is_required": bool(item.get("required", False)),
                    "order": int(item.get("sortOrder") or index),
                    "is_active": bool(item.get("isActive", True)),
                },
            )
        ContactFormField.objects.filter(section=section).exclude(slug__in=seen_fields).update(is_active=False)

        self._seed_text_items(section.phones, ContactPhone, section, contacts.get("phones", []), value_field="value", extra_fields=("label", "href"))
        self._seed_text_items(section.emails, ContactEmail, section, contacts.get("emails", []), value_field="value", extra_fields=("label", "href"))

    def _seed_footer(self, site_data: dict):
        footer = site_data.get("footer", {})
        meta = footer.get("meta", {})

        section = self._upsert(
            FooterSection,
            singleton_key=1,
            defaults={
                "is_active": True,
                "brand_name": self._clean_text(meta.get("brandName")),
                "brand_href": self._clean_text(meta.get("brandHref")) or "/",
                "support_email": self._clean_text(meta.get("supportEmail")),
                "nav_aria_label": self._clean_text(meta.get("navAriaLabel")),
                "logo_alt": self._clean_text(footer.get("media", {}).get("logo", {}).get("alt")),
            },
        )
        self._set_image(section, "logo", self._clean_text(footer.get("media", {}).get("logo", {}).get("src")), "footer")
        section.save()

        seen_columns = []
        for column_index, column in enumerate(footer.get("items", []), start=1):
            column_slug = self._clean_text(column.get("slug")) or f"footer-column-{column_index}"
            seen_columns.append(column_slug)
            column_obj = self._upsert(
                FooterColumn,
                section=section,
                slug=column_slug,
                defaults={
                    "title": self._clean_text(column.get("title")),
                    "order": int(column.get("sortOrder") or column_index),
                    "is_active": bool(column.get("isActive", True)),
                },
            )

            seen_links = []
            for link_index, link in enumerate(column.get("links", []), start=1):
                link_slug = self._clean_text(link.get("slug")) or f"{column_slug}-link-{link_index}"
                seen_links.append(link_slug)
                self._upsert(
                    FooterLink,
                    column=column_obj,
                    slug=link_slug,
                    defaults={
                        "label": self._clean_text(link.get("label")),
                        "href": self._clean_text(link.get("href")),
                        "order": int(link.get("sortOrder") or link_index),
                        "is_active": bool(link.get("isActive", True)),
                        "is_external": str(link.get("href", "")).startswith("http"),
                    },
                )
            FooterLink.objects.filter(column=column_obj).exclude(slug__in=seen_links).update(is_active=False)

        FooterColumn.objects.filter(section=section).exclude(slug__in=seen_columns).update(is_active=False)

    def _seed_policy_pages(self):
        mapping = {
            "privacy-policy": self.frontend_dir / "pages" / "privacy-policy.vue",
            "public-offer": self.frontend_dir / "pages" / "public-offer.vue",
            "user-agreement": self.frontend_dir / "pages" / "user-agreement.vue",
        }

        for slug, file_path in mapping.items():
            if not file_path.exists():
                continue

            content = file_path.read_text(encoding="utf-8")
            title = self._extract_first(content, r"<h1[^>]*>(.*?)</h1>")
            back_label = self._extract_first(content, r"<button[^>]*>(.*?)</button>")
            page = self._upsert(
                PolicyPage,
                slug=slug,
                defaults={
                    "title": self._html_to_text(title),
                    "back_button_label": self._html_to_text(back_label),
                    "is_active": True,
                },
            )

            sections = re.findall(r"<section[^>]*>(.*?)</section>", content, flags=re.S)
            seen_sections = []
            for section_index, section_html in enumerate(sections, start=1):
                heading = self._extract_first(section_html, r"<h2[^>]*>(.*?)</h2>")
                paragraph = self._extract_first(section_html, r"<p>(.*?)</p>")
                section_slug = f"{slug}-section-{section_index}"
                seen_sections.append(section_slug)
                section_obj = self._upsert(
                    PolicySection,
                    page=page,
                    slug=section_slug,
                    defaults={
                        "title": self._html_to_text(heading),
                        "order": section_index,
                        "is_active": True,
                    },
                )

                text_value = self._html_to_text(paragraph)
                paragraph_slug = f"{section_slug}-paragraph-1"
                self._upsert(
                    PolicyParagraph,
                    section=section_obj,
                    slug=paragraph_slug,
                    defaults={
                        "text": text_value,
                        "order": 1,
                        "is_active": True,
                    },
                )
                PolicyParagraph.objects.filter(section=section_obj).exclude(slug=paragraph_slug).update(is_active=False)

            PolicySection.objects.filter(page=page).exclude(slug__in=seen_sections).update(is_active=False)

    def _seed_text_items(self, manager, model, parent, items, value_field: str = "text", extra_fields: tuple[str, ...] = ()):
        seen = []
        parent_field = manager.field.name

        for index, item in enumerate(items, start=1):
            slug = self._clean_text(item.get("slug")) or f"{model.__name__.lower()}-{index}"
            seen.append(slug)

            defaults = {
                value_field: self._clean_text(item.get(value_field)),
                "order": int(item.get("sortOrder") or index),
                "is_active": bool(item.get("isActive", True)),
            }
            for field_name in extra_fields:
                defaults[field_name] = self._clean_text(item.get(field_name))

            self._upsert(
                model,
                **{parent_field: parent, "slug": slug},
                defaults=defaults,
            )

        model.objects.filter(**{parent_field: parent}).exclude(slug__in=seen).update(is_active=False)

    def _extract_first(self, text: str, pattern: str) -> str:
        match = re.search(pattern, text, flags=re.S)
        if not match:
            return ""
        return match.group(1)

    def _html_to_text(self, value: str) -> str:
        clean = re.sub(r"<[^>]+>", "", value or "")
        clean = html.unescape(clean)
        clean = re.sub(r"\s+", " ", clean)
        return clean.strip()
