from django.db import models

from apps.validators import validate_image_or_svg


class ChannelsSection(models.Model):
    title = models.TextField(verbose_name="Основной заголовок секции")
    subtitle = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Маленький бейдж сверху",
    )
    description = models.TextField(blank=True, default="", verbose_name="Описание")
    item_aria_label_prefix = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Префикс aria-label",
    )
    background = models.ImageField(upload_to="channels/", verbose_name="Фоновое изображение")
    image = models.ImageField(upload_to="channels/", verbose_name="Первое большое изображение")
    secondary_image = models.ImageField(
        upload_to="channels/",
        verbose_name="Второе большое изображение",
    )

    class Meta:
        verbose_name = "Как связаться с нами"
        verbose_name_plural = "Как связаться с нами"

    def __str__(self):
        return self.subtitle or (self.title[:80] if self.title else f"Как связаться с нами #{self.pk}")


class ChannelItem(models.Model):
    section = models.ForeignKey(
        ChannelsSection,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Как связаться с нами",
    )
    name = models.CharField(max_length=255, verbose_name="Название канала")
    icon = models.FileField(upload_to="channels/icons/", validators=[validate_image_or_svg], verbose_name="Иконка")
    href = models.CharField(max_length=500, verbose_name="Ссылка")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Канал связи"
        verbose_name_plural = "Каналы связи"
        ordering = ("sort_order", "id")

    def __str__(self):
        return self.name
