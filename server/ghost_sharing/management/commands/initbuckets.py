from django.core.management.base import BaseCommand

from hsutils.minio import prepare_buckets


class Command(BaseCommand):
    help = "Creates and initializes buckets for ghost data storage"

    def handle(self, *args, **options):
        self.stdout.write("Preparing buckets")
        prepare_buckets()
        self.stdout.write("Buckets prepared")
