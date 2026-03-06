from django.db import models


class SystemIntegrationsSection(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок секции")

    class Meta:
        verbose_name = "Секция интеграции с системами"
        verbose_name_plural = "Секция интеграции с системами"

    def __str__(self):
        return self.title


class SystemIntegrationItem(models.Model):
    section = models.ForeignKey(
        SystemIntegrationsSection,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Секция интеграции с системами",
    )
    title = models.CharField(max_length=255, verbose_name="Название интеграции")
    description = models.TextField(blank=True, default="", verbose_name="Описание интеграции")
    image = models.ImageField(upload_to="system_integrations/", verbose_name="Изображение")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Пункт интеграции"
        verbose_name_plural = "Пункты интеграции"
        ordering = ("sort_order", "id")

    def __str__(self):
        return self.title
