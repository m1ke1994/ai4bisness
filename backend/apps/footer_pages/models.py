from django.db import models


class FooterPage(models.Model):
    class PageKey(models.TextChoices):
        PRIVACY_POLICY = "privacy_policy", "Политика конфиденциальности"
        PUBLIC_OFFER = "public_offer", "Публичная оферта"
        USER_AGREEMENT = "user_agreement", "Пользовательское соглашение"

    class PageSlug(models.TextChoices):
        PRIVACY_POLICY = "privacy-policy", "Политика конфиденциальности"
        PUBLIC_OFFER = "public-offer", "Публичная оферта"
        USER_AGREEMENT = "user-agreement", "Пользовательское соглашение"

    key = models.CharField(
        max_length=32,
        unique=True,
        choices=PageKey.choices,
        verbose_name="Технический ключ",
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
        choices=PageSlug.choices,
        verbose_name="Slug",
    )
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст страницы")
    is_published = models.BooleanField(default=True, verbose_name="Опубликована")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Страница подвала"
        verbose_name_plural = "Страницы подвала"
        ordering = ("key", "id")

    def __str__(self):
        return self.title

