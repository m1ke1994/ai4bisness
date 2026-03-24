import logging
from datetime import date, time

import requests
from django.conf import settings

from apps.company_briefs.models import TelegramDeliveryStatus

logger = logging.getLogger(__name__)


def send_company_brief_pdf_to_telegram(
    *,
    pdf_bytes: bytes,
    file_name: str,
    company_name: str,
    preferred_contact_date: date | None,
    preferred_contact_time: time | None,
) -> dict[str, str]:
    bot_token = getattr(settings, "COMPANY_BRIEF_TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = str(getattr(settings, "COMPANY_BRIEF_TELEGRAM_CHAT_ID", "")).strip()

    if not bot_token or not chat_id:
        logger.info(
            "Telegram отправка анкеты пропущена: не заданы COMPANY_BRIEF_TELEGRAM_BOT_TOKEN/COMPANY_BRIEF_TELEGRAM_CHAT_ID."
        )
        return {"status": TelegramDeliveryStatus.SKIPPED, "error": ""}

    endpoint = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    date_text = (
        preferred_contact_date.strftime("%d.%m.%Y")
        if preferred_contact_date
        else "не указано"
    )
    time_text = (
        preferred_contact_time.strftime("%H:%M")
        if preferred_contact_time
        else "не указано"
    )
    caption = (
        f"Новая анкета от компании: {company_name}\n"
        f"Назначенное время связи: {date_text} {time_text}\n"
        "Во вложении PDF-файл с заполненной анкетой."
    )

    try:
        response = requests.post(
            endpoint,
            data={"chat_id": chat_id, "caption": caption},
            files={"document": (file_name, pdf_bytes, "application/pdf")},
            timeout=30,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.exception("Ошибка HTTP при отправке PDF анкеты в Telegram.")
        return {"status": TelegramDeliveryStatus.FAILED, "error": str(exc)}

    try:
        payload = response.json()
    except ValueError:
        logger.error("Telegram API вернул не-JSON ответ при отправке PDF анкеты.")
        return {
            "status": TelegramDeliveryStatus.FAILED,
            "error": "Telegram API вернул некорректный ответ.",
        }

    if not payload.get("ok"):
        error_description = str(payload.get("description") or "Telegram API вернул ошибку.")
        logger.error("Telegram API ошибка при отправке PDF анкеты: %s", error_description)
        return {"status": TelegramDeliveryStatus.FAILED, "error": error_description}

    return {"status": TelegramDeliveryStatus.SENT, "error": ""}
