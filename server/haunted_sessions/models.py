import uuid

from django.contrib.auth import get_user_model
from django.db import models

from hsutils import TimestampedModel

# Create your models here.
User = get_user_model()


class Tag(TimestampedModel):
    name = models.CharField(blank=False, null=False, max_length=128, unique=True)
    description = models.CharField(blank=False, null=False, max_length=512)

    def __str__(self):
        return self.name


class Session(TimestampedModel):
    key = models.UUIDField(default=uuid.uuid4, unique=True)
    owner = models.ForeignKey(to=User, on_delete=models.deletion.CASCADE)
    tags = models.ManyToManyField(to=Tag, related_name="sessions")
    description = models.CharField(blank=True, null=False, max_length=512)
    players = models.ManyToManyField(to=User, related_name="sessions")
