from django.contrib import admin

from .models import Announcement


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("message", "text_color", "background_color")


admin.site.register(Announcement, AnnouncementAdmin)
