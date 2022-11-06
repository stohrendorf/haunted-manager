import uuid

from django.contrib.auth import get_user_model
from django.db import models

from hsutils import TimestampedModel

User = get_user_model()


class ApiKey(TimestampedModel):
    owner = models.OneToOneField(to=User, on_delete=models.deletion.CASCADE)
    key = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return f"{self.owner}({self.key})"
