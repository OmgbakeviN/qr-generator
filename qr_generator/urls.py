import os
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("qr.urls")),
]

# Local dev
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Render / production demo (serve MEDIA through Django)
if os.environ.get("SERVE_MEDIA", "0") == "1":
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
