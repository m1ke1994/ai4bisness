from django.db import models


class HeaderSection(models.Model):
    is_enabled = models.BooleanField(default=True, verbose_name="Включено")
    brand_name = models.CharField(max_length=120, verbose_name="Название бренда")
    brand_href = models.CharField(max_length=255, default="/", verbose_name="Ссылка бренда")
    logo_image = models.ImageField(
        upload_to="header/logo/",
        blank=True,
        null=True,
        verbose_name="Логотип (файл)",
    )
    logo_url = models.URLField(blank=True, null=True, verbose_name="Логотип (URL)")
    logo_alt = models.CharField(max_length=160, blank=True, default="", verbose_name="Alt логотипа")

    desktop_nav_aria = models.CharField(
        max_length=160,
        blank=True,
        default="",
        verbose_name="ARIA: навигация (десктоп)",
    )
    mobile_dialog_aria = models.CharField(
        max_length=160,
        blank=True,
        default="",
        verbose_name="ARIA: диалог меню (мобильное)",
    )
    mobile_nav_aria = models.CharField(
        max_length=160,
        blank=True,
        default="",
        verbose_name="ARIA: навигация (мобильное)",
    )
    open_menu_aria = models.CharField(
        max_length=160,
        blank=True,
        default="",
        verbose_name="ARIA: открыть меню",
    )
    close_menu_aria = models.CharField(
        max_length=160,
        blank=True,
        default="",
        verbose_name="ARIA: закрыть меню",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Шапка сайта"
        verbose_name_plural = "Шапка сайта"

    def __str__(self) -> str:
        return self.brand_name or "Шапка сайта"

    def logo_src(self) -> str:
        if self.logo_image:
            return self.logo_image.url
        if self.logo_url:
            return self.logo_url
        return ""


class HeaderNavItem(models.Model):
    header = models.ForeignKey(
        HeaderSection,
        related_name="nav_items",
        on_delete=models.CASCADE,
        verbose_name="Шапка",
    )
    label = models.CharField(max_length=80, verbose_name="Название пункта")
    href = models.CharField(max_length=255, verbose_name="Ссылка (href)")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Пункт меню шапки"
        verbose_name_plural = "Пункты меню шапки"
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return f"{self.label} ({self.href})"


class HeaderSocialLink(models.Model):
    header = models.ForeignKey(
        HeaderSection,
        related_name="social_links",
        on_delete=models.CASCADE,
        verbose_name="Шапка",
    )
    href = models.URLField(max_length=500, verbose_name="Ссылка")
    aria_label = models.CharField(max_length=160, blank=True, default="", verbose_name="ARIA: описание")
    icon_image = models.ImageField(
        upload_to="header/social/",
        blank=True,
        null=True,
        verbose_name="Иконка (файл)",
    )
    icon_url = models.URLField(blank=True, null=True, verbose_name="Иконка (URL)")
    icon_alt = models.CharField(max_length=160, blank=True, default="", verbose_name="Alt иконки")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Соцссылка шапки"
        verbose_name_plural = "Соцссылки шапки"
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return self.aria_label or self.href or "Соцссылка"

    def icon_src(self) -> str:
        if self.icon_image:
            return self.icon_image.url
        if self.icon_url:
            return self.icon_url
        return ""
