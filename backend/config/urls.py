from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.core.urls")),
    path("api/", include("apps.footer.urls")),
    path("api/", include("apps.heroblock.urls")),
    path("api/", include("apps.pricing.urls")),
    path("api/", include("apps.reviews.urls")),
    path("api/", include("apps.contacts.urls")),
    path("api/", include("apps.integration_steps.urls")),
    path("api/", include("apps.channels.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
