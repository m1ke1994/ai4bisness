from django.db import models


class TelegramDeliveryStatus(models.TextChoices):
    PENDING = "pending", "Ожидает отправки"
    SENT = "sent", "Отправлено"
    SKIPPED = "skipped", "Пропущено"
    FAILED = "failed", "Ошибка"


class CompanyBrief(models.Model):
    company_name = models.CharField(max_length=255, verbose_name="Название компании")
    industry = models.CharField(max_length=255, verbose_name="Отрасль")
    subindustry = models.CharField(max_length=255, blank=True, verbose_name="Подотрасль")
    team_members = models.TextField(verbose_name="Члены команды")
    short_description = models.TextField(verbose_name="Краткое описание")
    full_description = models.TextField(verbose_name="Полное описание")

    primary_phone = models.CharField(max_length=64, verbose_name="Основной номер телефона")
    secondary_phone = models.CharField(max_length=64, blank=True, verbose_name="Дополнительный номер телефона")
    primary_email = models.EmailField(verbose_name="Основной email")
    support_email = models.EmailField(blank=True, verbose_name="Email поддержки")
    sales_email = models.EmailField(blank=True, verbose_name="Email продаж")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    city = models.CharField(max_length=120, verbose_name="Город")
    country = models.CharField(max_length=120, verbose_name="Страна")
    website_url = models.URLField(blank=True, verbose_name="URL веб-сайта")
    timezone_name = models.CharField(max_length=120, verbose_name="Часовой пояс")

    services = models.JSONField(default=list, verbose_name="Услуги")
    assistant_channels = models.JSONField(default=list, verbose_name="Каналы ассистента")
    crm_integrations = models.JSONField(default=list, verbose_name="CRM-интеграции")
    booking_integrations = models.JSONField(default=list, verbose_name="Интеграции бронирования")

    pdf_file = models.FileField(upload_to="company_briefs/pdfs/", blank=True, verbose_name="PDF анкеты")
    telegram_status = models.CharField(
        max_length=16,
        choices=TelegramDeliveryStatus.choices,
        default=TelegramDeliveryStatus.PENDING,
        verbose_name="Статус отправки в Telegram",
    )
    telegram_error = models.TextField(blank=True, verbose_name="Текст ошибки Telegram")
    source_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP отправителя")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    class Meta:
        verbose_name = "Анкета компании"
        verbose_name_plural = "Анкеты компаний"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.company_name} ({self.created_at:%d.%m.%Y %H:%M})"
