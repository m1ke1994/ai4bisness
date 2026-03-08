from django.urls import path

from apps.footer_pages.views import FooterPageDetailAPIView, FooterPageListAPIView

urlpatterns = [
    path("footer-pages/", FooterPageListAPIView.as_view(), name="footer-pages-list"),
    path("footer-pages/<slug:slug>/", FooterPageDetailAPIView.as_view(), name="footer-pages-detail"),
]

