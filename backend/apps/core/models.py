from django.db import models

from apps.validators import validate_image_or_svg


class SiteHeader(models.Model):
    logo = models.FileField(upload_to="header/", validators=[validate_image_or_svg], verbose_name="Логотип")
    logo_link = models.CharField(max_length=255, verbose_name="Ссылка с логотипа")
    brand_name = models.CharField(max_length=255, verbose_name="Название бренда")

    class Meta:
        verbose_name = "Шапка сайта"
        verbose_name_plural = "Шапка сайта"

    def __str__(self):
        return self.brand_name or f"Шапка сайта #{self.pk}"


class HeaderMenuLink(models.Model):
    header = models.ForeignKey(
        SiteHeader,
        on_delete=models.CASCADE,
        related_name="menu_items",
        verbose_name="Шапка сайта",
    )
    title = models.CharField(max_length=255, verbose_name="Название ссылки")
    href = models.CharField(max_length=255, verbose_name="Ссылка")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Ссылка меню шапки"
        verbose_name_plural = "Ссылки меню шапки"
        ordering = ("sort_order", "id")

    def __str__(self):
        return self.title
