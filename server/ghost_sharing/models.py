import uuid

from django.contrib.auth import get_user_model
from django.db import models

from haunted_sessions.models import Tag
from hsutils import TimestampedModel

User = get_user_model()


class GhostFinishType(models.TextChoices):
    unfinished = "Unfinished"
    death = "Death"
    completed = "Completed"


class Ghost(TimestampedModel):
    owner = models.ForeignKey(to=User, on_delete=models.deletion.PROTECT)
    file_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    level = models.CharField(max_length=64, null=False)
    tags = models.ManyToManyField(to=Tag, related_name="ghosts")
    hash = models.CharField(max_length=64, blank=True, null=False)
    published = models.BooleanField()
    downloads = models.PositiveIntegerField(default=0)
    data_size = models.PositiveIntegerField()
    finish_type = models.CharField(max_length=16, null=True, choices=GhostFinishType.choices)
    duration = models.DurationField()
    original_filename = models.CharField(max_length=64, blank=False)
    description = models.CharField(blank=False, null=False, max_length=512)
