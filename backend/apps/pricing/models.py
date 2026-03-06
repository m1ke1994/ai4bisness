from django.db import models


class PricingSection(models.Model):
    title = models.CharField(max_length=255, verbose_name="Основной заголовок блока")
    subtitle = models.CharField(max_length=255, blank=True, default="", verbose_name="Подзаголовок блока")
    channels_label = models.CharField(max_length=255, blank=True, default="", verbose_name="Подпись перед каналами")

    class Meta:
        verbose_name = "Секция тарифов"
        verbose_name_plural = "Секция тарифов"

    def __str__(self):
        return self.title


class PricingPlan(models.Model):
    pricing_section = models.ForeignKey(
        PricingSection,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Секция тарифов",
    )
    title = models.CharField(max_length=255, verbose_name="Название тарифа")
    subtitle = models.CharField(max_length=255, blank=True, default="", verbose_name="Подпись под названием")
    accent_badge = models.CharField(max_length=255, blank=True, default="", verbose_name="Акцентный бейдж")
    inherit_line = models.CharField(max_length=255, blank=True, default="", verbose_name="Строка наследования")
    channels = models.TextField(blank=True, default="", verbose_name="Каналы")
    cta_label = models.CharField(max_length=255, blank=True, default="", verbose_name="Текст кнопки")
    cta_link = models.CharField(max_length=500, blank=True, default="", verbose_name="Ссылка кнопки")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    is_featured = models.BooleanField(default=False, verbose_name="Выделенная карточка")
    is_dark_card = models.BooleanField(default=False, verbose_name="Темная карточка")

    class Meta:
        verbose_name = "Тарифный план"
        verbose_name_plural = "Тарифные планы"
        ordering = ("sort_order", "id")

    def __str__(self):
        return self.title


class PricingFeature(models.Model):
    plan = models.ForeignKey(
        PricingPlan,
        on_delete=models.CASCADE,
        related_name="features",
        verbose_name="Тарифный план",
    )
    text = models.CharField(max_length=500, verbose_name="Текст пункта")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Пункт тарифа"
        verbose_name_plural = "Пункты тарифа"
        ordering = ("sort_order", "id")

    def __str__(self):
        return self.text
