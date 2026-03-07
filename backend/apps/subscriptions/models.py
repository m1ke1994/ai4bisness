from django.db import models


class SubscriptionsSection(models.Model):
    title = models.CharField(max_length=255, verbose_name="\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a \u0441\u0435\u043a\u0446\u0438\u0438")
    subtitle_prefix = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="\u041f\u0440\u0435\u0444\u0438\u043a\u0441 \u043f\u043e\u0434\u0437\u0430\u0433\u043e\u043b\u043e\u0432\u043a\u0430",
    )
    subtitle_highlight = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="\u0410\u043a\u0446\u0435\u043d\u0442\u043d\u0430\u044f \u0447\u0430\u0441\u0442\u044c \u043f\u043e\u0434\u0437\u0430\u0433\u043e\u043b\u043e\u0432\u043a\u0430",
    )
    badge_primary = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="\u041f\u0435\u0440\u0432\u044b\u0439 \u0431\u0435\u0439\u0434\u0436",
    )
    badge_secondary = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="\u0412\u0442\u043e\u0440\u043e\u0439 \u0431\u0435\u0439\u0434\u0436",
    )
    description = models.TextField(blank=True, default="", verbose_name="\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0431\u043b\u043e\u043a\u0430")
    left_label = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="\u041f\u043e\u0434\u043f\u0438\u0441\u044c \u043b\u0435\u0432\u043e\u0439 \u043a\u043e\u043b\u043e\u043d\u043a\u0438",
    )
    right_label = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="\u041f\u043e\u0434\u043f\u0438\u0441\u044c \u043f\u0440\u0430\u0432\u043e\u0439 \u043a\u043e\u043b\u043e\u043d\u043a\u0438",
    )
    paid_title = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a \u043f\u0440\u0430\u0432\u043e\u0439 \u043a\u0430\u0440\u0442\u043e\u0447\u043a\u0438",
    )
    paid_description = models.TextField(
        blank=True,
        default="",
        verbose_name="\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043f\u0440\u0430\u0432\u043e\u0439 \u043a\u0430\u0440\u0442\u043e\u0447\u043a\u0438",
    )
    note_description = models.TextField(blank=True, default="", verbose_name="\u0422\u0435\u043a\u0441\u0442 \u043f\u0440\u0438\u043c\u0435\u0447\u0430\u043d\u0438\u044f")

    class Meta:
        verbose_name = "\u041f\u043b\u0430\u0442\u043d\u044b\u0435 \u0438 \u0431\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u044b\u0435 \u043f\u043e\u0434\u043f\u0438\u0441\u043a\u0438"
        verbose_name_plural = "\u041f\u043b\u0430\u0442\u043d\u044b\u0435 \u0438 \u0431\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u044b\u0435 \u043f\u043e\u0434\u043f\u0438\u0441\u043a\u0438"

    def __str__(self):
        return self.title


class SubscriptionItem(models.Model):
    section = models.ForeignKey(
        SubscriptionsSection,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="\u041f\u043b\u0430\u0442\u043d\u044b\u0435 \u0438 \u0431\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u044b\u0435 \u043f\u043e\u0434\u043f\u0438\u0441\u043a\u0438",
    )
    text = models.CharField(max_length=500, verbose_name="\u0422\u0435\u043a\u0441\u0442 \u043f\u0443\u043d\u043a\u0442\u0430")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="\u041f\u043e\u0440\u044f\u0434\u043e\u043a \u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u043a\u0438")
    is_active = models.BooleanField(default=True, verbose_name="\u0410\u043a\u0442\u0438\u0432\u043d\u043e")

    class Meta:
        verbose_name = "\u041f\u0443\u043d\u043a\u0442 \u043f\u043e\u0434\u043f\u0438\u0441\u043a\u0438"
        verbose_name_plural = "\u041f\u0443\u043d\u043a\u0442\u044b \u043f\u043e\u0434\u043f\u0438\u0441\u043a\u0438"
        ordering = ("sort_order", "id")

    def __str__(self):
        return self.text
