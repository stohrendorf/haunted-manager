from django.contrib import admin

from .models import Session, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


class SessionAdmin(admin.ModelAdmin):
    list_display = ("owner", "key", "description", "last_used")
    list_display_links = ("owner", "key")
    readonly_fields = ("last_used", "created_at")


admin.site.register(Tag, TagAdmin)
admin.site.register(Session, SessionAdmin)
