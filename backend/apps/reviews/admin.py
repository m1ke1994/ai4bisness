from django.contrib import admin

from apps.reviews.models import Review, ReviewsSection


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 1
    fields = (
        "company",
        "person",
        "preview_text",
        "preview_bullets",
        "details_text",
        "results",
        "sort_order",
        "is_active",
    )
    ordering = ("sort_order", "id")


@admin.register(ReviewsSection)
class ReviewsSectionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "subtitle", "read_more_label")
    search_fields = ("title", "subtitle", "read_more_label", "modal_results_title")
    inlines = (ReviewInline,)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("company", "person", "reviews_section", "sort_order", "is_active")
    list_filter = ("reviews_section", "is_active")
    search_fields = ("company", "person", "preview_text", "details_text")
    list_editable = ("sort_order", "is_active")
    ordering = ("sort_order", "id")
