from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("siteapi.urls")),
    path("", include("haunted_sessions.urls")),
    path("", include("haunted_auth.urls")),
    path("", include("ghost_sharing.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
