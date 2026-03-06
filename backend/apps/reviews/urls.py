from django.urls import path

from apps.reviews.views import ReviewsAPIView

urlpatterns = [
    path("reviews/", ReviewsAPIView.as_view(), name="reviews"),
]
