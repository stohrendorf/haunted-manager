import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from hsutils import TimestampedModel

# Create your models here.
User = get_user_model()


class Tag(TimestampedModel):
    name = models.CharField(blank=False, null=False, max_length=128, unique=True)
    description = models.CharField(blank=False, null=False, max_length=512)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Session(TimestampedModel):
    key = models.UUIDField(default=uuid.uuid4, unique=True)
    owner = models.ForeignKey(to=User, on_delete=models.deletion.CASCADE)
    tags = models.ManyToManyField(to=Tag, related_name="sessions")
    description = models.CharField(blank=True, null=False, max_length=512)
    players = models.ManyToManyField(to=User, related_name="sessions")
    start = models.DateTimeField(null=True, default=None)
    end = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return str(self.key)

    @property
    def is_event(self) -> bool:
        return self.start is not None and self.end is not None


@receiver(pre_save, sender=Session)
def update_timestamped_model_timestamps(sender, instance: Session, **kwargs):
    if instance.start is None or instance.end is None:
        instance.start = None
        instance.end = None
