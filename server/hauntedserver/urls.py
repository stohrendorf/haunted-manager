from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("siteapi.urls")),
    path("", include("haunted_sessions.urls")),
    path("", include("haunted_auth.urls")),
]
