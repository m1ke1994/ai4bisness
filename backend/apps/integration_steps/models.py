from django.db import models


class IntegrationStepsSection(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок секции")
    subtitle = models.CharField(max_length=255, blank=True, default="", verbose_name="Подзаголовок секции")
    cta_title_line_1 = models.CharField(max_length=255, blank=True, default="", verbose_name="Первая строка CTA")
    cta_title_line_2 = models.CharField(max_length=255, blank=True, default="", verbose_name="Вторая строка CTA")
    cta_background = models.ImageField(upload_to="integration_steps/", verbose_name="Фон CTA-карточки")
    cta_image = models.ImageField(upload_to="integration_steps/", verbose_name="Изображение CTA-карточки")

    class Meta:
        verbose_name = "Этапы интеграции"
        verbose_name_plural = "Этапы интеграции"

    def __str__(self):
        return self.title


class IntegrationStepItem(models.Model):
    steps_section = models.ForeignKey(
        IntegrationStepsSection,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Этапы интеграции",
    )
    day = models.CharField(max_length=50, verbose_name="Подпись дня")
    title = models.CharField(max_length=255, verbose_name="Название этапа")
    description = models.TextField(verbose_name="Описание этапа")
    image = models.ImageField(upload_to="integration_steps/", verbose_name="Изображение этапа")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Этап интеграции"
        verbose_name_plural = "Этапы интеграции"
        ordering = ("sort_order", "id")

    def __str__(self):
        return f"{self.day} - {self.title}"
