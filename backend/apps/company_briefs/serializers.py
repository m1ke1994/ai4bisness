import re
from decimal import Decimal, InvalidOperation

from django.utils import timezone
from rest_framework import serializers

from apps.company_briefs.models import CompanyBrief

PHONE_PATTERN = re.compile(r"^[0-9+\-\s()]{6,30}$")
PRICE_PATTERN = re.compile(r"^\d+(?:[.,]\d{1,2})?$")


def normalize_phone_value(value: str, field_label: str) -> str:
    normalized = str(value or "").strip()

    if not normalized:
        return ""

    if not PHONE_PATTERN.fullmatch(normalized):
        raise serializers.ValidationError(
            f"{field_label}: используйте телефон в формате +7 (999) 123-45-67."
        )

    return normalized


def normalize_choice_list(values: list[str]) -> list[str]:
    normalized: list[str] = []

    for value in values:
        item = str(value or "").strip()
        if item and item not in normalized:
            normalized.append(item)

    return normalized


class CompanyBriefServiceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, trim_whitespace=True)
    description = serializers.CharField(max_length=2000, trim_whitespace=True)
    price_from = serializers.CharField(max_length=64, required=False, allow_blank=True, default="")
    price_to = serializers.CharField(max_length=64, required=False, allow_blank=True, default="")

    @staticmethod
    def _parse_price(value: str, field_label: str) -> Decimal | None:
        raw_value = str(value or "").strip()
        if not raw_value:
            return None

        normalized = raw_value.replace(" ", "").replace(",", ".")
        if not PRICE_PATTERN.fullmatch(normalized):
            raise serializers.ValidationError(
                {field_label: "Введите корректную цену в формате 10000 или 10000.50."}
            )

        try:
            return Decimal(normalized)
        except InvalidOperation as exc:
            raise serializers.ValidationError(
                {field_label: "Введите корректную цену."}
            ) from exc

    def validate(self, attrs):
        price_from_value = str(attrs.get("price_from", "")).strip()
        price_to_value = str(attrs.get("price_to", "")).strip()

        parsed_price_from = self._parse_price(price_from_value, "price_from")
        parsed_price_to = self._parse_price(price_to_value, "price_to")

        if (
            parsed_price_from is not None
            and parsed_price_to is not None
            and parsed_price_from > parsed_price_to
        ):
            raise serializers.ValidationError(
                {"price_to": "Цена \"до\" должна быть больше или равна цене \"от\"."}
            )

        attrs["price_from"] = price_from_value.replace(",", ".")
        attrs["price_to"] = price_to_value.replace(",", ".")
        return attrs


class CompanyBriefCreateSerializer(serializers.ModelSerializer):
    services = CompanyBriefServiceSerializer(many=True, allow_empty=False)
    assistant_channels = serializers.ListField(
        child=serializers.CharField(max_length=120),
        allow_empty=False,
    )
    crm_integrations = serializers.ListField(
        child=serializers.CharField(max_length=120),
        allow_empty=True,
        required=False,
        default=list,
    )
    booking_integrations = serializers.ListField(
        child=serializers.CharField(max_length=120),
        allow_empty=True,
        required=False,
        default=list,
    )

    secondary_phone = serializers.CharField(
        max_length=64,
        required=False,
        allow_blank=True,
        default="",
    )
    support_email = serializers.EmailField(required=False, allow_blank=True, default="")
    sales_email = serializers.EmailField(required=False, allow_blank=True, default="")
    subindustry = serializers.CharField(max_length=255, required=False, allow_blank=True, default="")
    website_url = serializers.URLField(required=False, allow_blank=True, default="")
    preferred_contact_date = serializers.DateField(required=True)
    preferred_contact_time = serializers.TimeField(
        required=True,
        input_formats=["%H:%M", "%H:%M:%S"],
        format="%H:%M",
    )

    class Meta:
        model = CompanyBrief
        fields = (
            "company_name",
            "industry",
            "subindustry",
            "team_members",
            "short_description",
            "full_description",
            "primary_phone",
            "secondary_phone",
            "primary_email",
            "support_email",
            "sales_email",
            "address",
            "city",
            "country",
            "website_url",
            "timezone_name",
            "preferred_contact_date",
            "preferred_contact_time",
            "services",
            "assistant_channels",
            "crm_integrations",
            "booking_integrations",
        )

    def validate_primary_phone(self, value):
        return normalize_phone_value(value, "Основной номер телефона")

    def validate_secondary_phone(self, value):
        return normalize_phone_value(value, "Дополнительный номер телефона")

    def validate_services(self, value):
        normalized_services: list[dict] = []

        for index, service in enumerate(value, start=1):
            name = str(service.get("name") or "").strip()
            description = str(service.get("description") or "").strip()

            if not name:
                raise serializers.ValidationError(
                    f"Услуга #{index}: укажите наименование услуги."
                )

            if not description:
                raise serializers.ValidationError(
                    f"Услуга #{index}: укажите описание услуги."
                )

            normalized_services.append(
                {
                    "name": name,
                    "description": description,
                    "price_from": str(service.get("price_from") or "").strip(),
                    "price_to": str(service.get("price_to") or "").strip(),
                }
            )

        return normalized_services

    def validate_assistant_channels(self, value):
        normalized = normalize_choice_list(value)
        if not normalized:
            raise serializers.ValidationError("Выберите хотя бы один канал ассистента.")
        return normalized

    def validate_crm_integrations(self, value):
        return normalize_choice_list(value)

    def validate_booking_integrations(self, value):
        return normalize_choice_list(value)

    def validate(self, attrs):
        attrs = super().validate(attrs)

        preferred_contact_date = attrs.get("preferred_contact_date")
        preferred_contact_time = attrs.get("preferred_contact_time")

        if not preferred_contact_date:
            raise serializers.ValidationError(
                {"preferred_contact_date": "Выберите дату связи."}
            )

        if not preferred_contact_time:
            raise serializers.ValidationError(
                {"preferred_contact_time": "Выберите время связи."}
            )

        now = timezone.localtime()
        current_date = now.date()
        current_time = now.time().replace(second=0, microsecond=0)

        if preferred_contact_date < current_date:
            raise serializers.ValidationError(
                {
                    "preferred_contact_date": "Нельзя выбрать прошедшую дату. Выберите актуальную дату связи."
                }
            )

        if (
            preferred_contact_date == current_date
            and preferred_contact_time <= current_time
        ):
            raise serializers.ValidationError(
                {
                    "preferred_contact_time": "Выберите время связи позже текущего момента."
                }
            )

        return attrs

    def create(self, validated_data):
        return CompanyBrief.objects.create(**validated_data)
