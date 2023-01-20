from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from haunted_sessions.models import Session


class Command(BaseCommand):
    help = "Removes unused sessions"

    def handle(self, *args, **options):
        (total_deleted, objects_deleted) = Session.objects.filter(
            last_used__lt=timezone.now() - timedelta(weeks=settings.SESSION_RETENTION_WEEKS)
        ).delete()
        sessions_deleted = objects_deleted.get(Session._meta.label, 0)
        self.stdout.write(f"Deleted {total_deleted} objects, {sessions_deleted} sessions")
