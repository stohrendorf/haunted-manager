from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "Removes outdated users that failed to activate"

    def handle(self, *args, **options):
        User = get_user_model()
        (total_deleted, objects_deleted) = User.objects.filter(
            last_login__isnull=True,
            date_joined__lt=timezone.now() - timedelta(seconds=settings.EMAIL_MAIL_TOKEN_LIFE),
        ).delete()
        users_deleted = objects_deleted.get(get_user_model()._meta.label, 0)
        self.stdout.write(f"Deleted {total_deleted} objects, {users_deleted} users")
