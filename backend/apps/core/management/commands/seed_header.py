from django.core.management.base import BaseCommand

from apps.core.models import HeaderNavItem, HeaderSection, HeaderSocialLink


DEFAULT_NAV_ITEMS = [
    {"sort_order": 10, "label": "Преимущества", "href": "#advantages"},
    {"sort_order": 20, "label": "Интеграции", "href": "#integrations"},
    {"sort_order": 30, "label": "Тарифы", "href": "#pricing"},
    {"sort_order": 40, "label": "Шаги", "href": "#steps"},
    {"sort_order": 50, "label": "Отзывы", "href": "#reviews"},
    {"sort_order": 60, "label": "Контакты", "href": "#contacts"},
]

DEFAULT_SOCIAL_LINKS = [
    {"sort_order": 10, "aria_label": "Telegram", "icon_alt": "Telegram"},
    {"sort_order": 20, "aria_label": "WhatsApp", "icon_alt": "WhatsApp"},
    {"sort_order": 30, "aria_label": "Instagram", "icon_alt": "Instagram"},
]


class Command(BaseCommand):
    help = "Создает шапку сайта и заполняет пункты меню и соцссылки по умолчанию"

    def handle(self, *args, **options):
        header, created = HeaderSection.objects.get_or_create(
            id=1,
            defaults={
                "is_enabled": True,
                "brand_name": "Название бренда",
                "brand_href": "/",
                "logo_alt": "",
                "desktop_nav_aria": "",
                "mobile_dialog_aria": "",
                "mobile_nav_aria": "",
                "open_menu_aria": "",
                "close_menu_aria": "",
            },
        )

        if created:
            self.stdout.write(self.style.SUCCESS("Создана запись «Шапка сайта»."))
        else:
            self.stdout.write("Запись «Шапка сайта» уже существует.")

        for item in DEFAULT_NAV_ITEMS:
            HeaderNavItem.objects.update_or_create(
                header=header,
                sort_order=item["sort_order"],
                defaults={
                    "label": item["label"],
                    "href": item["href"],
                    "is_active": True,
                },
            )

        for link in DEFAULT_SOCIAL_LINKS:
            HeaderSocialLink.objects.update_or_create(
                header=header,
                sort_order=link["sort_order"],
                defaults={
                    "href": "",
                    "aria_label": link["aria_label"],
                    "icon_alt": link["icon_alt"],
                    "icon_url": None,
                    "is_active": True,
                },
            )

        self.stdout.write(self.style.SUCCESS("Шапка сайта заполнена значениями по умолчанию."))
