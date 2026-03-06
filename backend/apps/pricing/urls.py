from django.urls import path

from apps.pricing.views import PricingAPIView

urlpatterns = [
    path("pricing/", PricingAPIView.as_view(), name="pricing"),
]
