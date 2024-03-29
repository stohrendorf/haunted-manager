# Generated by Django 4.1.3 on 2022-11-26 08:06

import uuid

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("haunted_sessions", "0006_remove_session_is_event"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Ghost",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("file_id", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("level", models.CharField(max_length=64)),
                ("hash", models.CharField(blank=True, max_length=64)),
                ("published", models.BooleanField()),
                ("downloads", models.PositiveIntegerField(default=0)),
                ("data_size", models.PositiveIntegerField()),
                (
                    "finish_type",
                    models.CharField(
                        choices=[("Unfinished", "Unfinished"), ("Death", "Death"), ("Completed", "Completed")],
                        max_length=16,
                        null=True,
                    ),
                ),
                ("duration", models.DurationField()),
                ("original_filename", models.CharField(max_length=64)),
                ("description", models.CharField(max_length=512)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ("tags", models.ManyToManyField(related_name="ghosts", to="haunted_sessions.tag")),
            ],
            options={
                "ordering": ("created_at",),
                "get_latest_by": "created_at",
                "abstract": False,
            },
        ),
    ]
