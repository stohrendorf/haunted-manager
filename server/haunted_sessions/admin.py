from django.contrib import admin

from .models import Session, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


class SessionAdmin(admin.ModelAdmin):
    list_display = ("owner", "key", "description")
    list_display_links = ("owner", "key")


admin.site.register(Tag, TagAdmin)
admin.site.register(Session, SessionAdmin)
