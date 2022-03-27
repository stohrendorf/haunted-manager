from django.contrib import admin

from .models import Session, Tag


class TagAdmin(admin.ModelAdmin):
    pass


class SessionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tag, TagAdmin)
admin.site.register(Session, SessionAdmin)
