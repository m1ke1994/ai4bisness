from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        abstract = True


class SingletonModel(TimeStampedModel):
    singleton_key = models.PositiveSmallIntegerField(
        default=1,
        unique=True,
        editable=False,
        verbose_name="Ключ singleton",
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.singleton_key = 1
        return super().save(*args, **kwargs)


class OrderedItemModel(TimeStampedModel):
    slug = models.SlugField(max_length=120, blank=True, verbose_name="Slug")
    order = models.PositiveIntegerField(default=1, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        abstract = True
        ordering = ("order", "id")


class SiteSettings(SingletonModel):
    brand_name = models.CharField(max_length=120, verbose_name="Название бренда")
    site_name = models.CharField(max_length=120, blank=True, verbose_name="Название сайта")
    domain = models.CharField(max_length=255, blank=True, verbose_name="Домен")
    description = models.TextField(blank=True, verbose_name="Описание")
    locale = models.CharField(max_length=16, default="ru-RU", verbose_name="Локаль")
    theme = models.CharField(max_length=32, default="light", verbose_name="Тема")
    support_email = models.EmailField(blank=True, verbose_name="Email поддержки")
    contact_form_open_event = models.CharField(
        max_length=120,
        default="contact-feedback-form:open",
        verbose_name="Событие открытия формы",
    )
    logo = models.ImageField(upload_to="site/", blank=True, null=True, verbose_name="Логотип")
    logo_alt = models.CharField(max_length=180, blank=True, verbose_name="Alt логотипа")
    favicon = models.ImageField(upload_to="site/", blank=True, null=True, verbose_name="Фавикон")

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self) -> str:
        return self.brand_name or "Настройки сайта"


class HeaderSection(SingletonModel):
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    brand_href = models.CharField(max_length=255, default="/", verbose_name="Ссылка бренда")
    aria_desktop_nav = models.CharField(max_length=160, blank=True, verbose_name="ARIA: десктоп-навигация")
    aria_mobile_nav = models.CharField(max_length=160, blank=True, verbose_name="ARIA: мобильная навигация")
    aria_mobile_dialog = models.CharField(max_length=160, blank=True, verbose_name="ARIA: мобильный диалог")
    aria_open_menu = models.CharField(max_length=160, blank=True, verbose_name="ARIA: открыть меню")
    aria_close_menu = models.CharField(max_length=160, blank=True, verbose_name="ARIA: закрыть меню")

    class Meta:
        verbose_name = "Секция: Шапка"
        verbose_name_plural = "Секция: Шапка"

    def __str__(self) -> str:
        return "Шапка"


class HeaderNavItem(OrderedItemModel):
    section = models.ForeignKey(
        HeaderSection,
        on_delete=models.CASCADE,
        related_name="nav_items",
        verbose_name="Секция",
    )
    label = models.CharField(max_length=120, verbose_name="Текст")
    href = models.CharField(max_length=255, verbose_name="Ссылка")
    is_external = models.BooleanField(default=False, verbose_name="Внешняя ссылка")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Пункт меню шапки"
        verbose_name_plural = "Пункты меню шапки"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_header_nav_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.label


class HeaderMobileSocialItem(OrderedItemModel):
    section = models.ForeignKey(
        HeaderSection,
        on_delete=models.CASCADE,
        related_name="mobile_social_items",
        verbose_name="Секция",
    )
    label = models.CharField(max_length=120, verbose_name="Название")
    href = models.CharField(max_length=500, verbose_name="Ссылка")
    aria_label = models.CharField(max_length=180, blank=True, verbose_name="ARIA-метка")
    icon = models.ImageField(upload_to="header/mobile_social/", blank=True, null=True, verbose_name="Иконка")
    icon_alt = models.CharField(max_length=180, blank=True, verbose_name="Alt иконки")
    is_external = models.BooleanField(default=True, verbose_name="Внешняя ссылка")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Соцссылка мобильного меню"
        verbose_name_plural = "Соцссылки мобильного меню"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_header_mobile_social_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.label


class HeroSection(SingletonModel):
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    subtitle = models.CharField(max_length=255, verbose_name="Подзаголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    stats_disclaimer = models.TextField(blank=True, verbose_name="Дисклеймер статистики")
    phone_alt = models.CharField(max_length=180, blank=True, verbose_name="Alt изображения телефона")
    phone_image = models.ImageField(upload_to="hero/", blank=True, null=True, verbose_name="Изображение телефона")
    texture_image = models.ImageField(upload_to="hero/", blank=True, null=True, verbose_name="Текстура фона")
    texture_alt = models.CharField(max_length=180, blank=True, verbose_name="Alt текстуры")
    image_vars = models.JSONField(default=dict, blank=True, verbose_name="CSS переменные изображения")

    class Meta:
        verbose_name = "Секция: Hero"
        verbose_name_plural = "Секция: Hero"

    def __str__(self) -> str:
        return "Hero"


class HeroStatItem(OrderedItemModel):
    section = models.ForeignKey(
        HeroSection,
        on_delete=models.CASCADE,
        related_name="stats",
        verbose_name="Секция",
    )
    value = models.CharField(max_length=80, verbose_name="Значение")
    text = models.CharField(max_length=255, verbose_name="Подпись")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Показатель Hero"
        verbose_name_plural = "Показатели Hero"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_hero_stat_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return f"{self.value} — {self.text}"


class HeroLogosSection(SingletonModel):
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Секция: Логотипы под Hero"
        verbose_name_plural = "Секция: Логотипы под Hero"

    def __str__(self) -> str:
        return "Логотипы под Hero"


class HeroLogoItem(OrderedItemModel):
    section = models.ForeignKey(
        HeroLogosSection,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Секция",
    )
    logo = models.ImageField(upload_to="hero/logos/", blank=True, null=True, verbose_name="Логотип")
    logo_alt = models.CharField(max_length=180, blank=True, verbose_name="Alt логотипа")
    source_path = models.CharField(max_length=255, blank=True, verbose_name="Исходный путь")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Логотип под Hero"
        verbose_name_plural = "Логотипы под Hero"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_hero_logo_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.slug or f"Логотип {self.id}"

class AdvantagesSection(SingletonModel):
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    training_badge = models.CharField(max_length=255, verbose_name="Бейдж обучения")
    training_right_pill = models.CharField(max_length=255, blank=True, verbose_name="Плашка справа")
    training_right_title = models.TextField(blank=True, verbose_name="Заголовок справа")

    summary_title = models.CharField(max_length=255, verbose_name="Заголовок сравнения")
    summary_subtitle = models.CharField(max_length=255, blank=True, verbose_name="Подзаголовок сравнения")
    summary_description = models.TextField(blank=True, verbose_name="Подпись под таблицей")

    desktop_stage_label = models.CharField(max_length=120, blank=True, verbose_name="Desktop: Этап")
    desktop_ai_label = models.CharField(max_length=120, blank=True, verbose_name="Desktop: ИИ")
    desktop_human_label = models.CharField(max_length=120, blank=True, verbose_name="Desktop: Менеджер")
    mobile_title = models.CharField(max_length=255, blank=True, verbose_name="Mobile: Заголовок")
    mobile_subtitle = models.CharField(max_length=255, blank=True, verbose_name="Mobile: Подзаголовок")
    mobile_ai_label = models.CharField(max_length=120, blank=True, verbose_name="Mobile: ИИ")
    mobile_human_label = models.CharField(max_length=120, blank=True, verbose_name="Mobile: Менеджер")
    mobile_footer = models.CharField(max_length=255, blank=True, verbose_name="Mobile: Подпись")
    stage_description_label = models.CharField(max_length=255, blank=True, verbose_name="Подпись этапа")

    check_icon = models.ImageField(upload_to="advantages/", blank=True, null=True, verbose_name="Иконка check")
    check_icon_alt = models.CharField(max_length=180, blank=True, verbose_name="Alt иконки")

    class Meta:
        verbose_name = "Секция: Преимущества"
        verbose_name_plural = "Секция: Преимущества"

    def __str__(self) -> str:
        return "Преимущества"


class AdvantagesStatItem(OrderedItemModel):
    section = models.ForeignKey(
        AdvantagesSection,
        on_delete=models.CASCADE,
        related_name="stats",
        verbose_name="Секция",
    )
    value = models.CharField(max_length=80, verbose_name="Значение")
    text = models.CharField(max_length=255, verbose_name="Текст")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Статистика преимуществ"
        verbose_name_plural = "Статистика преимуществ"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_advantages_stat_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return f"{self.value} — {self.text}"


class TrainingSourceItem(OrderedItemModel):
    section = models.ForeignKey(
        AdvantagesSection,
        on_delete=models.CASCADE,
        related_name="training_sources",
        verbose_name="Секция",
    )
    title = models.CharField(max_length=180, verbose_name="Источник")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Источник обучения"
        verbose_name_plural = "Источники обучения"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_training_source_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.title


class TrainingRightBulletItem(OrderedItemModel):
    section = models.ForeignKey(
        AdvantagesSection,
        on_delete=models.CASCADE,
        related_name="training_right_bullets",
        verbose_name="Секция",
    )
    text = models.TextField(verbose_name="Текст")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Пункт справа"
        verbose_name_plural = "Пункты справа"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_training_right_bullet_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.text[:80]


class ComparisonRowItem(OrderedItemModel):
    section = models.ForeignKey(
        AdvantagesSection,
        on_delete=models.CASCADE,
        related_name="comparison_rows",
        verbose_name="Секция",
    )
    title = models.CharField(max_length=180, verbose_name="Этап")
    ai_description = models.TextField(verbose_name="Описание ИИ")
    human_description = models.TextField(verbose_name="Описание менеджера")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Строка сравнения"
        verbose_name_plural = "Строки сравнения"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_comparison_row_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.title


class AdvantagesAiSummaryItem(OrderedItemModel):
    section = models.ForeignKey(
        AdvantagesSection,
        on_delete=models.CASCADE,
        related_name="ai_summary_items",
        verbose_name="Секция",
    )
    text = models.TextField(verbose_name="Текст")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Пункт AI Summary"
        verbose_name_plural = "Пункты AI Summary"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_ai_summary_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.text[:80]


class AdvantagesHumanLimitItem(OrderedItemModel):
    section = models.ForeignKey(
        AdvantagesSection,
        on_delete=models.CASCADE,
        related_name="human_limit_items",
        verbose_name="Секция",
    )
    text = models.TextField(verbose_name="Текст")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Пункт Human Limits"
        verbose_name_plural = "Пункты Human Limits"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_human_limit_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.text[:80]


class AiValueSection(SingletonModel):
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    subtitle_prefix = models.CharField(max_length=120, blank=True, verbose_name="Префикс подзаголовка")
    subtitle_highlight = models.CharField(max_length=120, blank=True, verbose_name="Акцент подзаголовка")
    description = models.TextField(blank=True, verbose_name="Описание")

    launch_badge_primary = models.CharField(max_length=180, blank=True, verbose_name="Бейдж primary")
    launch_badge_secondary = models.CharField(max_length=180, blank=True, verbose_name="Бейдж secondary")
    launch_title = models.CharField(max_length=255, blank=True, verbose_name="Заголовок launch")
    launch_description = models.TextField(blank=True, verbose_name="Описание launch")
    launch_left_label = models.CharField(max_length=120, blank=True, verbose_name="Лейбл левой колонки")
    launch_right_label = models.CharField(max_length=120, blank=True, verbose_name="Лейбл правой колонки")
    launch_paid_title = models.CharField(max_length=255, blank=True, verbose_name="Заголовок paid")
    launch_paid_description = models.TextField(blank=True, verbose_name="Описание paid")
    launch_note_title = models.CharField(max_length=255, blank=True, verbose_name="Заголовок note")
    launch_note_description = models.TextField(blank=True, verbose_name="Описание note")

    integrations_title = models.CharField(max_length=255, blank=True, verbose_name="Заголовок интеграций")
    integrations_subtitle = models.CharField(max_length=255, blank=True, verbose_name="Подзаголовок интеграций")
    integrations_add_aria_label = models.CharField(max_length=160, blank=True, verbose_name="ARIA add")
    integrations_banner = models.ImageField(upload_to="ai_value/", blank=True, null=True, verbose_name="Баннер интеграций")
    integrations_banner_alt = models.CharField(max_length=180, blank=True, verbose_name="Alt баннера")

    class Meta:
        verbose_name = "Секция: AI Value"
        verbose_name_plural = "Секция: AI Value"

    def __str__(self) -> str:
        return "AI Value"


class AiValuePointItem(OrderedItemModel):
    section = models.ForeignKey(
        AiValueSection,
        on_delete=models.CASCADE,
        related_name="value_points",
        verbose_name="Секция",
    )
    text = models.TextField(verbose_name="Текст")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Пункт ценности AI"
        verbose_name_plural = "Пункты ценности AI"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_ai_value_point_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.text[:80]


class AiIntegrationItem(OrderedItemModel):
    section = models.ForeignKey(
        AiValueSection,
        on_delete=models.CASCADE,
        related_name="integrations",
        verbose_name="Секция",
    )
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to="ai_value/integrations/", blank=True, null=True, verbose_name="Изображение")
    image_alt = models.CharField(max_length=180, blank=True, verbose_name="Alt изображения")
    source_path = models.CharField(max_length=255, blank=True, verbose_name="Исходный путь")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Интеграция AI"
        verbose_name_plural = "Интеграции AI"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_ai_integration_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.title

class ChannelsSection(SingletonModel):
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    title = models.CharField(max_length=255, blank=True, verbose_name="Заголовок")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Подзаголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    item_aria_label_prefix = models.CharField(max_length=120, blank=True, verbose_name="Префикс ARIA")

    background_image = models.ImageField(upload_to="channels/", blank=True, null=True, verbose_name="Фон секции")
    background_alt = models.CharField(max_length=180, blank=True, verbose_name="Alt фона")
    primary_phone_image = models.ImageField(upload_to="channels/", blank=True, null=True, verbose_name="Телефон (основной)")
    primary_phone_alt = models.CharField(max_length=180, blank=True, verbose_name="Alt основного телефона")
    secondary_phone_image = models.ImageField(upload_to="channels/", blank=True, null=True, verbose_name="Телефон (дополнительно)")
    secondary_phone_alt = models.CharField(max_length=180, blank=True, verbose_name="Alt дополнительного телефона")

    class Meta:
        verbose_name = "Секция: Каналы"
        verbose_name_plural = "Секция: Каналы"

    def __str__(self) -> str:
        return "Каналы"


class ChannelItem(OrderedItemModel):
    section = models.ForeignKey(
        ChannelsSection,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Секция",
    )
    name = models.CharField(max_length=120, verbose_name="Название")
    href = models.CharField(max_length=500, verbose_name="Ссылка")
    icon = models.ImageField(upload_to="channels/icons/", blank=True, null=True, verbose_name="Иконка")
    icon_alt = models.CharField(max_length=180, blank=True, verbose_name="Alt иконки")
    is_external = models.BooleanField(default=True, verbose_name="Внешняя ссылка")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_channel_item_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.name


class StepsSection(SingletonModel):
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Подзаголовок")

    cta_title = models.CharField(max_length=255, blank=True, verbose_name="CTA заголовок")
    cta_button_label = models.CharField(max_length=120, blank=True, verbose_name="CTA кнопка")
    cta_button_href = models.CharField(max_length=255, default="#contacts", verbose_name="CTA ссылка")

    cta_image = models.ImageField(upload_to="steps/", blank=True, null=True, verbose_name="CTA изображение")
    cta_image_alt = models.CharField(max_length=180, blank=True, verbose_name="Alt CTA изображения")
    cta_image_source_path = models.CharField(max_length=255, blank=True, verbose_name="CTA исходный путь")
    cta_background_image = models.ImageField(upload_to="steps/", blank=True, null=True, verbose_name="CTA фон")
    cta_background_alt = models.CharField(max_length=180, blank=True, verbose_name="Alt CTA фона")

    class Meta:
        verbose_name = "Секция: Этапы"
        verbose_name_plural = "Секция: Этапы"

    def __str__(self) -> str:
        return "Этапы"


class StepItem(OrderedItemModel):
    section = models.ForeignKey(
        StepsSection,
        on_delete=models.CASCADE,
        related_name="steps",
        verbose_name="Секция",
    )
    day = models.CharField(max_length=120, blank=True, verbose_name="День/период")
    title = models.CharField(max_length=255, blank=True, verbose_name="Заголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to="steps/items/", blank=True, null=True, verbose_name="Изображение")
    image_alt = models.CharField(max_length=180, blank=True, verbose_name="Alt изображения")
    source_path = models.CharField(max_length=255, blank=True, verbose_name="Исходный путь")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Этап"
        verbose_name_plural = "Этапы"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_step_item_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.title or self.day or f"Этап {self.order}"


class StepCtaActionItem(OrderedItemModel):
    section = models.ForeignKey(
        StepsSection,
        on_delete=models.CASCADE,
        related_name="cta_actions",
        verbose_name="Секция",
    )
    label = models.CharField(max_length=120, verbose_name="Текст")
    href = models.CharField(max_length=500, verbose_name="Ссылка")
    aria_label = models.CharField(max_length=180, blank=True, verbose_name="ARIA-метка")
    is_external = models.BooleanField(default=True, verbose_name="Внешняя ссылка")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "CTA действие этапов"
        verbose_name_plural = "CTA действия этапов"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_step_cta_action_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.label


class PricingSection(SingletonModel):
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Подзаголовок")
    channels_label = models.CharField(max_length=120, default="Каналы:", verbose_name="Подпись каналов")

    class Meta:
        verbose_name = "Секция: Тарифы"
        verbose_name_plural = "Секция: Тарифы"

    def __str__(self) -> str:
        return "Тарифы"


class PricingPlan(OrderedItemModel):
    section = models.ForeignKey(
        PricingSection,
        on_delete=models.CASCADE,
        related_name="plans",
        verbose_name="Секция",
    )
    title = models.CharField(max_length=120, verbose_name="Название тарифа")
    subtitle = models.CharField(max_length=180, blank=True, verbose_name="Подпись тарифа")
    channels = models.CharField(max_length=255, blank=True, verbose_name="Каналы")
    accent_badge = models.CharField(max_length=120, blank=True, verbose_name="Акцентный бейдж")
    inherit_line = models.CharField(max_length=180, blank=True, verbose_name="Строка наследования")
    featured = models.BooleanField(default=False, verbose_name="Избранный")
    dark_card = models.BooleanField(default=False, verbose_name="Тёмная карточка")
    cta_label = models.CharField(max_length=120, blank=True, verbose_name="Текст кнопки")
    cta_href = models.CharField(max_length=255, default="#contacts", verbose_name="Ссылка кнопки")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_pricing_plan_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.title


class PricingPlanFeature(OrderedItemModel):
    plan = models.ForeignKey(
        PricingPlan,
        on_delete=models.CASCADE,
        related_name="features",
        verbose_name="Тариф",
    )
    text = models.TextField(verbose_name="Текст")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Пункт тарифа"
        verbose_name_plural = "Пункты тарифа"
        constraints = [
            models.UniqueConstraint(
                fields=("plan", "slug"),
                name="unique_pricing_feature_slug_per_plan",
            )
        ]

    def __str__(self) -> str:
        return self.text[:80]

class ReviewsSection(SingletonModel):
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Подзаголовок")

    action_read_more = models.CharField(max_length=120, blank=True, verbose_name="Кнопка: читать далее")
    action_close_modal_aria = models.CharField(max_length=180, blank=True, verbose_name="ARIA: закрыть модалку")
    action_prev_page_aria = models.CharField(max_length=180, blank=True, verbose_name="ARIA: предыдущая страница")
    action_next_page_aria = models.CharField(max_length=180, blank=True, verbose_name="ARIA: следующая страница")
    action_pagination_aria = models.CharField(max_length=180, blank=True, verbose_name="ARIA: пагинация")
    action_pagination_go_to = models.CharField(max_length=180, blank=True, verbose_name="ARIA: перейти к странице")
    modal_results_title = models.CharField(max_length=120, blank=True, verbose_name="Заголовок результатов")

    class Meta:
        verbose_name = "Секция: Отзывы"
        verbose_name_plural = "Секция: Отзывы"

    def __str__(self) -> str:
        return "Отзывы"


class ReviewItem(OrderedItemModel):
    section = models.ForeignKey(
        ReviewsSection,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Секция",
    )
    company = models.CharField(max_length=180, verbose_name="Компания")
    person = models.CharField(max_length=255, blank=True, verbose_name="Кто оставил отзыв")
    rating = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Рейтинг")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_review_item_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.company


class ReviewPreviewParagraph(OrderedItemModel):
    review = models.ForeignKey(
        ReviewItem,
        on_delete=models.CASCADE,
        related_name="preview_paragraphs",
        verbose_name="Отзыв",
    )
    text = models.TextField(verbose_name="Текст")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Параграф превью"
        verbose_name_plural = "Параграфы превью"
        constraints = [
            models.UniqueConstraint(
                fields=("review", "slug"),
                name="unique_review_preview_paragraph_slug_per_review",
            )
        ]

    def __str__(self) -> str:
        return self.text[:80]


class ReviewPreviewBullet(OrderedItemModel):
    review = models.ForeignKey(
        ReviewItem,
        on_delete=models.CASCADE,
        related_name="preview_bullets",
        verbose_name="Отзыв",
    )
    text = models.TextField(verbose_name="Текст")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Буллет превью"
        verbose_name_plural = "Буллеты превью"
        constraints = [
            models.UniqueConstraint(
                fields=("review", "slug"),
                name="unique_review_preview_bullet_slug_per_review",
            )
        ]

    def __str__(self) -> str:
        return self.text[:80]


class ReviewDetailParagraph(OrderedItemModel):
    review = models.ForeignKey(
        ReviewItem,
        on_delete=models.CASCADE,
        related_name="detail_paragraphs",
        verbose_name="Отзыв",
    )
    text = models.TextField(verbose_name="Текст")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Параграф полной версии"
        verbose_name_plural = "Параграфы полной версии"
        constraints = [
            models.UniqueConstraint(
                fields=("review", "slug"),
                name="unique_review_detail_paragraph_slug_per_review",
            )
        ]

    def __str__(self) -> str:
        return self.text[:80]


class ReviewResultItem(OrderedItemModel):
    review = models.ForeignKey(
        ReviewItem,
        on_delete=models.CASCADE,
        related_name="results",
        verbose_name="Отзыв",
    )
    text = models.TextField(verbose_name="Текст")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Результат отзыва"
        verbose_name_plural = "Результаты отзыва"
        constraints = [
            models.UniqueConstraint(
                fields=("review", "slug"),
                name="unique_review_result_slug_per_review",
            )
        ]

    def __str__(self) -> str:
        return self.text[:80]


class ContactsSection(SingletonModel):
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Акцент заголовка")
    heading_line3 = models.CharField(max_length=255, blank=True, verbose_name="Третья строка заголовка")
    description = models.TextField(blank=True, verbose_name="Описание")

    card_title_line1 = models.CharField(max_length=255, blank=True, verbose_name="Карточка: строка 1")
    card_title_line2 = models.CharField(max_length=255, blank=True, verbose_name="Карточка: строка 2")
    card_response_time = models.CharField(max_length=255, blank=True, verbose_name="Карточка: время ответа")

    section_background_image = models.ImageField(upload_to="contacts/", blank=True, null=True, verbose_name="Фон секции")
    section_background_alt = models.CharField(max_length=180, blank=True, verbose_name="Alt фона секции")
    card_background_image = models.ImageField(upload_to="contacts/", blank=True, null=True, verbose_name="Фон карточки")
    card_background_alt = models.CharField(max_length=180, blank=True, verbose_name="Alt фона карточки")

    form_title = models.CharField(max_length=255, blank=True, verbose_name="Заголовок формы")
    form_subtitle = models.TextField(blank=True, verbose_name="Подзаголовок формы")
    form_submit_label = models.CharField(max_length=120, blank=True, verbose_name="Кнопка формы")
    form_close_aria_label = models.CharField(max_length=160, blank=True, verbose_name="ARIA закрытия формы")

    class Meta:
        verbose_name = "Секция: Контакты"
        verbose_name_plural = "Секция: Контакты"

    def __str__(self) -> str:
        return "Контакты"


class ContactMessenger(OrderedItemModel):
    section = models.ForeignKey(
        ContactsSection,
        on_delete=models.CASCADE,
        related_name="messengers",
        verbose_name="Секция",
    )
    name = models.CharField(max_length=120, verbose_name="Системное имя")
    label = models.CharField(max_length=120, verbose_name="Текст")
    href = models.CharField(max_length=500, verbose_name="Ссылка")
    icon = models.ImageField(upload_to="contacts/messengers/", blank=True, null=True, verbose_name="Иконка")
    icon_alt = models.CharField(max_length=180, blank=True, verbose_name="Alt иконки")
    aria_label = models.CharField(max_length=180, blank=True, verbose_name="ARIA-метка")
    message = models.TextField(blank=True, verbose_name="Текст сообщения")
    is_external = models.BooleanField(default=True, verbose_name="Внешняя ссылка")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Мессенджер"
        verbose_name_plural = "Мессенджеры"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_contact_messenger_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.label


class ContactFormField(OrderedItemModel):
    FIELD_TYPE_TEXT = "text"
    FIELD_TYPE_TEXTAREA = "textarea"
    FIELD_TYPE_EMAIL = "email"
    FIELD_TYPE_TEL = "tel"
    FIELD_TYPE_CHOICES = (
        (FIELD_TYPE_TEXT, "Text"),
        (FIELD_TYPE_TEXTAREA, "Textarea"),
        (FIELD_TYPE_EMAIL, "Email"),
        (FIELD_TYPE_TEL, "Tel"),
    )

    section = models.ForeignKey(
        ContactsSection,
        on_delete=models.CASCADE,
        related_name="form_fields",
        verbose_name="Секция",
    )
    field_key = models.CharField(max_length=50, verbose_name="Ключ")
    label = models.CharField(max_length=120, verbose_name="Лейбл")
    placeholder = models.CharField(max_length=255, blank=True, verbose_name="Placeholder")
    field_type = models.CharField(max_length=20, choices=FIELD_TYPE_CHOICES, default=FIELD_TYPE_TEXT, verbose_name="Тип поля")
    is_required = models.BooleanField(default=False, verbose_name="Обязательное")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Поле формы контактов"
        verbose_name_plural = "Поля формы контактов"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_contact_form_field_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.label


class ContactPhone(OrderedItemModel):
    section = models.ForeignKey(
        ContactsSection,
        on_delete=models.CASCADE,
        related_name="phones",
        verbose_name="Секция",
    )
    label = models.CharField(max_length=120, verbose_name="Лейбл")
    value = models.CharField(max_length=120, verbose_name="Значение")
    href = models.CharField(max_length=255, blank=True, verbose_name="Ссылка")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Телефон"
        verbose_name_plural = "Телефоны"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_contact_phone_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.value


class ContactEmail(OrderedItemModel):
    section = models.ForeignKey(
        ContactsSection,
        on_delete=models.CASCADE,
        related_name="emails",
        verbose_name="Секция",
    )
    label = models.CharField(max_length=120, verbose_name="Лейбл")
    value = models.EmailField(verbose_name="Email")
    href = models.CharField(max_length=255, blank=True, verbose_name="Ссылка")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Email"
        verbose_name_plural = "Email"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_contact_email_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.value

class FooterSection(SingletonModel):
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    brand_name = models.CharField(max_length=120, blank=True, verbose_name="Название бренда")
    brand_href = models.CharField(max_length=255, default="/", verbose_name="Ссылка бренда")
    support_email = models.EmailField(blank=True, verbose_name="Email поддержки")
    nav_aria_label = models.CharField(max_length=160, blank=True, verbose_name="ARIA навигации")
    logo = models.ImageField(upload_to="footer/", blank=True, null=True, verbose_name="Логотип")
    logo_alt = models.CharField(max_length=180, blank=True, verbose_name="Alt логотипа")

    class Meta:
        verbose_name = "Секция: Футер"
        verbose_name_plural = "Секция: Футер"

    def __str__(self) -> str:
        return "Футер"


class FooterColumn(OrderedItemModel):
    section = models.ForeignKey(
        FooterSection,
        on_delete=models.CASCADE,
        related_name="columns",
        verbose_name="Секция",
    )
    title = models.CharField(max_length=120, verbose_name="Заголовок")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Колонка футера"
        verbose_name_plural = "Колонки футера"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_footer_column_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.title


class FooterLink(OrderedItemModel):
    column = models.ForeignKey(
        FooterColumn,
        on_delete=models.CASCADE,
        related_name="links",
        verbose_name="Колонка",
    )
    label = models.CharField(max_length=180, verbose_name="Текст")
    href = models.CharField(max_length=500, verbose_name="Ссылка")
    is_external = models.BooleanField(default=False, verbose_name="Внешняя ссылка")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Ссылка футера"
        verbose_name_plural = "Ссылки футера"
        constraints = [
            models.UniqueConstraint(
                fields=("column", "slug"),
                name="unique_footer_link_slug_per_column",
            )
        ]

    def __str__(self) -> str:
        return self.label


class PolicyPage(TimeStampedModel):
    slug = models.SlugField(max_length=60, unique=True, verbose_name="Slug")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    back_button_label = models.CharField(max_length=120, default="← Вернуться назад", verbose_name="Текст кнопки назад")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        ordering = ("slug",)
        verbose_name = "Страница документа"
        verbose_name_plural = "Страницы документов"

    def __str__(self) -> str:
        return self.title


class PolicySection(OrderedItemModel):
    page = models.ForeignKey(
        PolicyPage,
        on_delete=models.CASCADE,
        related_name="sections",
        verbose_name="Страница",
    )
    title = models.CharField(max_length=255, verbose_name="Заголовок раздела")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Раздел документа"
        verbose_name_plural = "Разделы документа"
        constraints = [
            models.UniqueConstraint(
                fields=("page", "slug"),
                name="unique_policy_section_slug_per_page",
            )
        ]

    def __str__(self) -> str:
        return self.title


class PolicyParagraph(OrderedItemModel):
    section = models.ForeignKey(
        PolicySection,
        on_delete=models.CASCADE,
        related_name="paragraphs",
        verbose_name="Раздел",
    )
    text = models.TextField(verbose_name="Текст")

    class Meta(OrderedItemModel.Meta):
        verbose_name = "Параграф документа"
        verbose_name_plural = "Параграфы документа"
        constraints = [
            models.UniqueConstraint(
                fields=("section", "slug"),
                name="unique_policy_paragraph_slug_per_section",
            )
        ]

    def __str__(self) -> str:
        return self.text[:80]
