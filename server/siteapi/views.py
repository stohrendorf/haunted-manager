from datetime import timedelta

from django.conf import settings
from django.db.models import Sum
from django.http import HttpRequest

from ghost_sharing.models import Ghost
from haunted_sessions.models import Session
from hsutils.viewmodels import (
    AnnouncementEntry,
    AnnouncementsResponse,
    ServerInfoResponse,
)

from .models import Announcement, User


def get_announcements(request: HttpRequest) -> AnnouncementsResponse:
    return AnnouncementsResponse(
        announcements=[
            AnnouncementEntry(
                message=a.message,
                background_color=a.background_color,
                text_color=a.text_color,
            )
            for a in Announcement.objects.all()
        ],
    )


def get_server_info(request: HttpRequest) -> ServerInfoResponse:
    return ServerInfoResponse(
        total_users=User.objects.filter(is_active=True).count(),
        total_sessions=Session.objects.count(),
        total_ghosts=Ghost.objects.count(),
        total_ghost_duration=int(
            (Ghost.objects.all().aggregate(Sum("duration"))["duration__sum"] or timedelta(seconds=0)).total_seconds()
        ),
        coop_url=settings.COOP_SERVER_URL,
    )
