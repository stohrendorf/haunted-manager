from django.contrib import admin

from .models import Ghost


class GhostAdmin(admin.ModelAdmin):
    readonly_fields = ("file_id", "created_at", "hash")
    list_display = ("id", "created_at", "owner", "level", "finish_type", "published")
    list_filter = ("published", "level")


admin.site.register(Ghost, GhostAdmin)
