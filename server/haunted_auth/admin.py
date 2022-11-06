from django.contrib import admin

from .models import ApiKey


class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ("owner", "key")
    list_display_links = ("owner", "key")


admin.site.register(ApiKey, ApiKeyAdmin)
