from django.db import models


class ReviewsSection(models.Model):
    title = models.CharField(max_length=255, verbose_name="Основной заголовок секции")
    subtitle = models.CharField(max_length=255, blank=True, default="", verbose_name="Вторая строка заголовка")
    modal_results_title = models.CharField(max_length=255, blank=True, default="", verbose_name="Заголовок блока результатов")
    read_more_label = models.CharField(max_length=255, blank=True, default="", verbose_name="Текст кнопки")
    prev_page_aria = models.CharField(max_length=255, blank=True, default="", verbose_name="Aria-подпись кнопки назад")
    next_page_aria = models.CharField(max_length=255, blank=True, default="", verbose_name="Aria-подпись кнопки вперед")
    pagination_aria = models.CharField(max_length=255, blank=True, default="", verbose_name="Aria-подпись блока пагинации")
    pagination_go_to_label = models.CharField(max_length=255, blank=True, default="", verbose_name="Aria-переход к странице")
    close_modal_aria = models.CharField(max_length=255, blank=True, default="", verbose_name="Aria-подпись кнопки закрытия")

    class Meta:
        verbose_name = "Секция отзывов"
        verbose_name_plural = "Секция отзывов"

    def __str__(self):
        return self.title


class Review(models.Model):
    reviews_section = models.ForeignKey(
        ReviewsSection,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Секция отзывов",
    )
    company = models.CharField(max_length=255, verbose_name="Название компании")
    person = models.CharField(max_length=255, verbose_name="Подпись")
    preview_text = models.TextField(blank=True, default="", verbose_name="Краткий вводный текст")
    preview_bullets = models.JSONField(default=list, blank=True, verbose_name="Список тезисов превью")
    details_text = models.TextField(blank=True, default="", verbose_name="Полный текст отзыва")
    results = models.JSONField(default=list, blank=True, verbose_name="Список результатов")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ("sort_order", "id")

    def __str__(self):
        return f"{self.company} - {self.person}"
