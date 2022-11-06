from django.http import HttpRequest

from haunted_sessions.models import Session
from hsutils.viewmodels import AnnouncementEntry, AnnouncementsResponse, StatsResponse

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


def get_stats(request: HttpRequest) -> StatsResponse:
    return StatsResponse(
        total_users=User.objects.count(),
        total_sessions=Session.objects.count(),
    )
