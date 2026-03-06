from django.db import models


class SiteFooter(models.Model):
    logo = models.ImageField(upload_to="footer/", verbose_name="Логотип")
    logo_link = models.CharField(max_length=255, verbose_name="Ссылка с логотипа")
    brand_name = models.CharField(max_length=255, verbose_name="Название бренда")

    class Meta:
        verbose_name = "Подвал сайта"
        verbose_name_plural = "Подвал сайта"

    def __str__(self):
        return self.brand_name or f"Подвал сайта #{self.pk}"


class FooterLink(models.Model):
    footer = models.ForeignKey(
        SiteFooter,
        on_delete=models.CASCADE,
        related_name="links",
        verbose_name="Подвал сайта",
    )
    title = models.CharField(max_length=255, verbose_name="Название ссылки")
    href = models.CharField(max_length=255, verbose_name="Ссылка")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Ссылка подвала сайта"
        verbose_name_plural = "Ссылки подвала сайта"
        ordering = ("sort_order", "id")

    def __str__(self):
        return self.title
