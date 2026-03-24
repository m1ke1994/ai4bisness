from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

from django.utils import timezone
import reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from apps.company_briefs.models import CompanyBrief


def _resolve_fonts() -> tuple[str, str]:
    regular_name = "BriefSans"
    bold_name = "BriefSansBold"

    if regular_name in pdfmetrics.getRegisteredFontNames() and bold_name in pdfmetrics.getRegisteredFontNames():
        return regular_name, bold_name

    local_fonts_dir = Path(__file__).resolve().parent.parent / "assets" / "fonts"
    reportlab_fonts_dir = Path(reportlab.__file__).resolve().parent / "fonts"

    font_pairs = [
        (local_fonts_dir / "DejaVuSans.ttf", local_fonts_dir / "DejaVuSans-Bold.ttf"),
        (reportlab_fonts_dir / "Vera.ttf", reportlab_fonts_dir / "VeraBd.ttf"),
        (
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ),
        (
            Path("C:/Windows/Fonts/arial.ttf"),
            Path("C:/Windows/Fonts/arialbd.ttf"),
        ),
    ]

    for regular_path, bold_path in font_pairs:
        if regular_path.exists() and bold_path.exists():
            pdfmetrics.registerFont(TTFont(regular_name, str(regular_path)))
            pdfmetrics.registerFont(TTFont(bold_name, str(bold_path)))
            return regular_name, bold_name

    return "Helvetica", "Helvetica-Bold"


def _value_or_dash(value) -> str:
    text = str(value or "").strip()
    if not text:
        return "—"
    return text


def _paragraph_text(value: str) -> str:
    return escape(value).replace("\n", "<br/>")


def _build_styles(font_regular: str, font_bold: str) -> dict[str, ParagraphStyle]:
    base_styles = getSampleStyleSheet()

    return {
        "title": ParagraphStyle(
            "title",
            parent=base_styles["Heading1"],
            fontName=font_bold,
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#111218"),
            spaceAfter=10,
        ),
        "meta": ParagraphStyle(
            "meta",
            parent=base_styles["Normal"],
            fontName=font_regular,
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#67708A"),
            spaceAfter=4,
        ),
        "section_title": ParagraphStyle(
            "section_title",
            parent=base_styles["Heading2"],
            fontName=font_bold,
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#2B2E45"),
            spaceAfter=8,
            spaceBefore=12,
        ),
        "cell_label": ParagraphStyle(
            "cell_label",
            parent=base_styles["Normal"],
            fontName=font_bold,
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#4C5677"),
        ),
        "cell_value": ParagraphStyle(
            "cell_value",
            parent=base_styles["Normal"],
            fontName=font_regular,
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#181C2B"),
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base_styles["Normal"],
            fontName=font_regular,
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#181C2B"),
            leftIndent=12,
            spaceAfter=4,
        ),
    }


def _build_two_column_table(rows: list[tuple[str, str]], styles: dict[str, ParagraphStyle]) -> Table:
    table_rows = [
        [
            Paragraph(_paragraph_text(label), styles["cell_label"]),
            Paragraph(_paragraph_text(_value_or_dash(value)), styles["cell_value"]),
        ]
        for label, value in rows
    ]

    table = Table(table_rows, colWidths=[58 * mm, 122 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F4F6FD")),
                ("BACKGROUND", (1, 0), (1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#DDE2F1")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5EAF6")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def _price_range(price_from: str, price_to: str) -> str:
    from_value = _value_or_dash(price_from)
    to_value = _value_or_dash(price_to)

    if from_value == "—" and to_value == "—":
        return "Не указано"

    if from_value != "—" and to_value != "—":
        return f"{from_value} - {to_value}"

    if from_value != "—":
        return f"от {from_value}"

    return f"до {to_value}"


def build_company_brief_pdf(brief: CompanyBrief) -> bytes:
    font_regular, font_bold = _resolve_fonts()
    styles = _build_styles(font_regular, font_bold)

    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
        title="Анкета для компаний",
        author="AI4Business",
    )

    story = [
        Paragraph("Анкета для компаний", styles["title"]),
        Paragraph(
            _paragraph_text(
                f"Дата отправки: {timezone.localtime(brief.created_at).strftime('%d.%m.%Y %H:%M')}"
            ),
            styles["meta"],
        ),
        Paragraph(
            _paragraph_text("Документ сформирован автоматически на основании заполненной формы."),
            styles["meta"],
        ),
        Spacer(1, 6),
    ]

    story.append(Paragraph("Основные", styles["section_title"]))
    story.append(
        _build_two_column_table(
            [
                ("Название компании", brief.company_name),
                ("Отрасль", brief.industry),
                ("Подотрасль", brief.subindustry),
                ("Члены команды", brief.team_members),
                ("Краткое описание", brief.short_description),
                ("Полное описание", brief.full_description),
            ],
            styles,
        )
    )

    story.append(Paragraph("Контакты", styles["section_title"]))
    story.append(
        _build_two_column_table(
            [
                ("Основной номер телефона", brief.primary_phone),
                ("Дополнительный номер телефона", brief.secondary_phone),
                ("Основной e-mail", brief.primary_email),
                ("E-mail поддержки", brief.support_email),
                ("E-mail продаж", brief.sales_email),
                ("Адрес", brief.address),
                ("Город", brief.city),
                ("Страна", brief.country),
                ("URL веб-сайта", brief.website_url),
                ("Часовой пояс", brief.timezone_name),
            ],
            styles,
        )
    )

    story.append(Paragraph("Услуги", styles["section_title"]))
    service_rows = [["Услуга", "Описание", "Стоимость"]]
    for service in brief.services:
        service_rows.append(
            [
                _value_or_dash(service.get("name")),
                _value_or_dash(service.get("description")),
                _price_range(service.get("price_from", ""), service.get("price_to", "")),
            ]
        )

    service_table = Table(
        [
            [
                Paragraph(_paragraph_text(row[0]), styles["cell_label"] if idx == 0 else styles["cell_value"]),
                Paragraph(_paragraph_text(row[1]), styles["cell_label"] if idx == 0 else styles["cell_value"]),
                Paragraph(_paragraph_text(row[2]), styles["cell_label"] if idx == 0 else styles["cell_value"]),
            ]
            for idx, row in enumerate(service_rows)
        ],
        colWidths=[45 * mm, 95 * mm, 40 * mm],
    )
    service_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EDFF")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#2B2E45")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#DDE2F1")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5EAF6")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(service_table)

    story.append(Paragraph("Ассистенты", styles["section_title"]))
    assistant_channels = brief.assistant_channels or []
    if assistant_channels:
        for channel in assistant_channels:
            story.append(Paragraph(_paragraph_text(f"• {channel}"), styles["bullet"]))
    else:
        story.append(Paragraph(_paragraph_text("• Не выбрано"), styles["bullet"]))

    story.append(Paragraph("Интеграции", styles["section_title"]))
    crm_integrations = brief.crm_integrations or []
    booking_integrations = brief.booking_integrations or []

    if crm_integrations:
        story.append(Paragraph(_paragraph_text("CRM и системы"), styles["cell_label"]))
        for integration in crm_integrations:
            story.append(Paragraph(_paragraph_text(f"• {integration}"), styles["bullet"]))

    if booking_integrations:
        story.append(Paragraph(_paragraph_text("Бронирование"), styles["cell_label"]))
        for integration in booking_integrations:
            story.append(Paragraph(_paragraph_text(f"• {integration}"), styles["bullet"]))

    if not crm_integrations and not booking_integrations:
        story.append(Paragraph(_paragraph_text("• Не выбрано"), styles["bullet"]))

    document.build(story)
    return buffer.getvalue()
