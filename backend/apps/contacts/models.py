from django.db import models


class ContactsSection(models.Model):
    title = models.CharField(max_length=255, verbose_name="Первая строка заголовка")
    subtitle = models.CharField(max_length=255, verbose_name="Вторая строка заголовка")
    heading_line_3 = models.CharField(max_length=255, verbose_name="Третья строка заголовка")
    description = models.TextField(verbose_name="Описание")
    section_background = models.ImageField(upload_to="contacts/", verbose_name="Фон секции")
    card_background = models.ImageField(upload_to="contacts/", verbose_name="Фон карточки")
    channels_title = models.CharField(max_length=255, verbose_name="Первая строка заголовка карточки")
    channels_subtitle = models.CharField(max_length=255, verbose_name="Вторая строка заголовка карточки")

    class Meta:
        verbose_name = "Секция контактов"
        verbose_name_plural = "Секция контактов"

    def __str__(self):
        return self.title


class ContactChannel(models.Model):
    contacts_section = models.ForeignKey(
        ContactsSection,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Секция контактов",
    )
    name = models.CharField(max_length=255, verbose_name="Название канала")
    icon = models.ImageField(upload_to="contacts/icons/", verbose_name="Иконка")
    href = models.CharField(max_length=500, verbose_name="Ссылка")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Канал связи"
        verbose_name_plural = "Каналы связи"
        ordering = ("sort_order", "id")

    def __str__(self):
        return self.name
