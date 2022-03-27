from django.contrib.auth import get_user_model
from django.db import models

from hsutils import TimestampedModel

User = get_user_model()


class BootstrapBackgroundColor(models.TextChoices):
    primary = "primary"
    secondary = "secondary"
    success = "success"
    danger = "danger"
    warning = "warning"
    info = "info"
    light = "light"
    dark = "dark"


class BootstrapTextColor(models.TextChoices):
    white = "white"
    black = "black"


class Announcement(TimestampedModel):
    message = models.TextField(blank=False)
    background_color = models.CharField(
        max_length=16,
        blank=False,
        choices=BootstrapBackgroundColor.choices,
        default=BootstrapBackgroundColor.light,
    )
    text_color = models.CharField(
        max_length=16,
        blank=False,
        choices=BootstrapTextColor.choices,
        default=BootstrapTextColor.black,
    )
