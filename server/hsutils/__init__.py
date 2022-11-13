import logging
from functools import wraps
from typing import Callable, Concatenate, ParamSpec, TypeVar

from dataclasses_json import DataClassJsonMixin
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpRequest, HttpResponse, HttpResponseServerError, JsonResponse
from django.http.response import HttpResponseBase
from django.utils import timezone

T = TypeVar("T", bound=DataClassJsonMixin)
P = ParamSpec("P")


def json_response(
    handler: Callable[Concatenate[HttpRequest, P], HttpResponse | T | tuple[int, T]],
) -> Callable[Concatenate[HttpRequest, P], HttpResponseBase]:
    @wraps(handler)
    def wrapper(request: HttpRequest, *args: P.args, **kwargs: P.kwargs) -> HttpResponseBase:
        try:
            response_data = handler(request, *args, **kwargs)
        except Exception:
            logging.error("request processing error", exc_info=True)
            return JsonResponse(
                data={},
                status=HttpResponseServerError.status_code,
            )
        if isinstance(response_data, HttpResponseBase):
            return response_data

        response_code = HttpResponseBase.status_code
        if isinstance(response_data, tuple):
            response_code, response_data = response_data

        response_data.validate()

        return JsonResponse(
            data=response_data.to_dict(),
            status=response_code,
        )

    return wrapper


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False, blank=False, null=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False, blank=False, null=False)

    class Meta:
        abstract = True
        get_latest_by = "created_at"


@receiver(pre_save, sender=TimestampedModel)
def update_timestamped_model_timestamps(sender, instance: TimestampedModel, **kwargs):
    instance.updated_at = timezone.now()
