from django.conf import settings
from django.http import HttpRequest

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
        total_users=User.objects.count(),
        total_sessions=Session.objects.count(),
        coop_url=settings.COOP_SERVER_URL,
    )
