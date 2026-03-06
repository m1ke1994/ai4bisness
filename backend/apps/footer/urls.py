from django.urls import path

from apps.footer.views import FooterAPIView

urlpatterns = [
    path("footer/", FooterAPIView.as_view(), name="footer"),
]
