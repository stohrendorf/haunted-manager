from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False, blank=False, null=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False, blank=False, null=False)

    class Meta:
        abstract = True
        get_latest_by = "created_at"
        ordering = ("created_at",)


@receiver(pre_save, sender=TimestampedModel)
def update_timestamped_model_timestamps(sender, instance: TimestampedModel, **kwargs):
    instance.updated_at = timezone.now()
