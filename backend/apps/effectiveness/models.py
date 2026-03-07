from django.db import models


class EffectivenessSection(models.Model):
    training_title = models.CharField(max_length=255, verbose_name="Заголовок блока обучения")
    training_right_pill = models.CharField(max_length=255, blank=True, default="", verbose_name="Бейдж справа")
    training_right_title = models.CharField(max_length=255, blank=True, default="", verbose_name="Текст правой карточки")

    summary_subtitle = models.CharField(max_length=255, blank=True, default="", verbose_name="Подзаголовок сравнения")
    summary_title = models.CharField(max_length=255, blank=True, default="", verbose_name="Заголовок сравнения")
    desktop_stage_label = models.CharField(max_length=255, blank=True, default="", verbose_name="Desktop: заголовок колонки этапа")
    desktop_ai_label = models.CharField(max_length=255, blank=True, default="", verbose_name="Desktop: заголовок колонки AI")
    desktop_human_label = models.CharField(max_length=255, blank=True, default="", verbose_name="Desktop: заголовок колонки Human")
    mobile_ai_label = models.CharField(max_length=255, blank=True, default="", verbose_name="Mobile: подпись AI")
    mobile_human_label = models.CharField(max_length=255, blank=True, default="", verbose_name="Mobile: подпись Human")
    stage_description_label = models.CharField(max_length=255, blank=True, default="", verbose_name="Подпись описания этапа")
    desktop_footer = models.TextField(blank=True, default="", verbose_name="Нижний текст desktop")

    class Meta:
        verbose_name = "Эффективность"
        verbose_name_plural = "Эффективность"

    def __str__(self):
        return self.summary_title or self.training_title


class TrainingItem(models.Model):
    section = models.ForeignKey(
        EffectivenessSection,
        on_delete=models.CASCADE,
        related_name="training_items",
        verbose_name="Эффективность",
    )
    title = models.CharField(max_length=500, verbose_name="Текст пункта")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Пункт обучения"
        verbose_name_plural = "Пункты обучения"
        ordering = ("sort_order", "id")

    def __str__(self):
        return self.title


class CompareItem(models.Model):
    section = models.ForeignKey(
        EffectivenessSection,
        on_delete=models.CASCADE,
        related_name="compare_items",
        verbose_name="Эффективность",
    )
    title = models.CharField(max_length=255, verbose_name="Название этапа")
    ai_description = models.TextField(blank=True, default="", verbose_name="Описание AI")
    human_description = models.TextField(blank=True, default="", verbose_name="Описание Human")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Пункт сравнения"
        verbose_name_plural = "Пункты сравнения"
        ordering = ("sort_order", "id")

    def __str__(self):
        return self.title
