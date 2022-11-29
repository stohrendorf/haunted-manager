from django.contrib import admin

from .models import Gameflow, Ghost, Level


class GhostAdmin(admin.ModelAdmin):
    readonly_fields = ("file_id", "created_at", "hash")
    list_display = ("id", "created_at", "owner", "level", "finish_type", "published")
    list_filter = ("published", "level")


class LevelAdmin(admin.ModelAdmin):
    pass


class GameflowAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ghost, GhostAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Gameflow, GameflowAdmin)
