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


class Gameflow(TimestampedModel):
    identifier = models.CharField(max_length=64, null=False, blank=False, unique=True)
    title = models.CharField(max_length=128, null=False, blank=False)

    def __str__(self):
        return f"{self.identifier} - {self.title}"


class Level(TimestampedModel):
    gameflow = models.ForeignKey(to=Gameflow, related_name="levels", null=False, on_delete=models.PROTECT)
    identifier = models.CharField(max_length=64, null=False, blank=False)
    title = models.CharField(max_length=128, null=False, blank=False)

    def __str__(self):
        return f"{self.gameflow} - {self.identifier} - {self.title}"

    class Meta:
        unique_together = ("gameflow", "identifier")


class Ghost(TimestampedModel):
    owner = models.ForeignKey(to=User, on_delete=models.deletion.PROTECT)
    file_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    level = models.ForeignKey(to=Level, related_name="ghosts", null=False, on_delete=models.PROTECT)
    tags = models.ManyToManyField(to=Tag, related_name="ghosts")
    hash = models.CharField(max_length=64, blank=True, null=False)
    published = models.BooleanField()
    downloads = models.PositiveIntegerField(default=0)
    data_size = models.PositiveIntegerField()
    finish_type = models.CharField(max_length=16, null=True, choices=GhostFinishType.choices)
    duration = models.DurationField()
    original_filename = models.CharField(max_length=64, blank=False)
    description = models.CharField(blank=False, null=False, max_length=512)
