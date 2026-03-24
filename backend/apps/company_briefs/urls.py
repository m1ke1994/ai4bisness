from django.urls import path

from apps.company_briefs.views import CompanyBriefCreateAPIView

urlpatterns = [
    path("company-briefs/", CompanyBriefCreateAPIView.as_view(), name="company-briefs-create"),
]
