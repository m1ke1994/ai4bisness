from django.db import models


class HeroBlock(models.Model):
    title = models.CharField(max_length=255, verbose_name="Основной заголовок")
    subtitle = models.CharField(max_length=255, verbose_name="Подзаголовок")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="heroblock/", verbose_name="Основное изображение")
    stats_disclaimer = models.TextField(verbose_name="Текст под карточками статистики")

    class Meta:
        verbose_name = "Hero блок"
        verbose_name_plural = "Hero блок"

    def __str__(self):
        return self.title


class HeroStatItem(models.Model):
    hero_block = models.ForeignKey(
        HeroBlock,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Hero блок",
    )
    value = models.CharField(max_length=50, verbose_name="Значение")
    text = models.CharField(max_length=255, verbose_name="Текст")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Показатель Hero-блока"
        verbose_name_plural = "Показатели Hero-блока"
        ordering = ("sort_order", "id")

    def __str__(self):
        return f"{self.value} - {self.text}"
