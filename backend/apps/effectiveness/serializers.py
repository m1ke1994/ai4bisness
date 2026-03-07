from rest_framework import serializers

from apps.effectiveness.models import CompareItem, EffectivenessSection, TrainingItem


class TrainingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingItem
        fields = ("title",)


class CompareItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompareItem
        fields = ("title", "ai_description", "human_description")


class EffectivenessSectionSerializer(serializers.ModelSerializer):
    training = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()

    class Meta:
        model = EffectivenessSection
        fields = ("training", "summary")

    def get_training(self, obj):
        items = obj.training_items.filter(is_active=True).order_by("sort_order", "id")
        return {
            "title": obj.training_title,
            "right_pill": obj.training_right_pill,
            "right_title": obj.training_right_title,
            "items": TrainingItemSerializer(items, many=True).data,
        }

    def get_summary(self, obj):
        items = obj.compare_items.filter(is_active=True).order_by("sort_order", "id")
        return {
            "subtitle": obj.summary_subtitle,
            "title": obj.summary_title,
            "desktop_stage_label": obj.desktop_stage_label,
            "desktop_ai_label": obj.desktop_ai_label,
            "desktop_human_label": obj.desktop_human_label,
            "mobile_ai_label": obj.mobile_ai_label,
            "mobile_human_label": obj.mobile_human_label,
            "stage_description_label": obj.stage_description_label,
            "desktop_footer": obj.desktop_footer,
            "items": CompareItemSerializer(items, many=True).data,
        }
