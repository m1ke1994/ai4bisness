import logging

from django.core.files.base import ContentFile
from django.utils import timezone
from django.utils.text import slugify
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.company_briefs.models import TelegramDeliveryStatus
from apps.company_briefs.serializers import CompanyBriefCreateSerializer
from apps.company_briefs.services.pdf_service import build_company_brief_pdf
from apps.company_briefs.services.telegram_service import send_company_brief_pdf_to_telegram

logger = logging.getLogger(__name__)


def get_client_ip(request) -> str | None:
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    remote_addr = request.META.get("REMOTE_ADDR", "")
    return remote_addr.strip() or None


def build_pdf_file_name(company_name: str, brief_id: int) -> str:
    slug = slugify(company_name)[:60] or "company-brief"
    timestamp = timezone.localtime().strftime("%Y%m%d_%H%M%S")
    return f"{slug}-{brief_id}-{timestamp}.pdf"


class CompanyBriefCreateAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = CompanyBriefCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "message": "Проверьте заполнение обязательных полей и исправьте ошибки формы.",
                    "errors": serializer.errors,
                },
                status=400,
            )

        brief = serializer.save(source_ip=get_client_ip(request))

        try:
            pdf_bytes = build_company_brief_pdf(brief)
        except Exception:
            logger.exception("Не удалось сформировать PDF для анкеты компании #%s.", brief.pk)
            return Response(
                {
                    "message": "Анкета сохранена, но не удалось сформировать PDF. Попробуйте повторить отправку позже.",
                },
                status=500,
            )

        pdf_file_name = build_pdf_file_name(brief.company_name, brief.pk)
        brief.pdf_file.save(pdf_file_name, ContentFile(pdf_bytes), save=False)

        telegram_result = send_company_brief_pdf_to_telegram(
            pdf_bytes=pdf_bytes,
            file_name=pdf_file_name,
            company_name=brief.company_name,
            preferred_contact_date=brief.preferred_contact_date,
            preferred_contact_time=brief.preferred_contact_time,
        )

        brief.telegram_status = telegram_result["status"]
        brief.telegram_error = telegram_result.get("error", "")
        brief.save(update_fields=("pdf_file", "telegram_status", "telegram_error"))

        if brief.telegram_status == TelegramDeliveryStatus.FAILED:
            return Response(
                {
                    "message": "Анкета сохранена, но уведомление в Telegram отправить не удалось. Мы получили данные и обработаем заявку вручную.",
                },
                status=502,
            )

        return Response(
            {
                "message": "Анкета успешно отправлена. Спасибо!",
                "id": brief.pk,
                "telegram_status": (
                    brief.telegram_status.value
                    if hasattr(brief.telegram_status, "value")
                    else brief.telegram_status
                ),
            },
            status=201,
        )
