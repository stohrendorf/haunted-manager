import logging
from functools import wraps
from typing import Any, Callable, TypeVar

from dataclasses_json import DataClassJsonMixin
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseServerError,
    JsonResponse,
)
from django.http.response import HttpResponseBase
from django.utils import timezone

T = TypeVar("T", bound=DataClassJsonMixin)

RequestHandler = Callable[[HttpRequest], HttpResponse | T | tuple[int, T]]
HttpResponseRequestHandler = Callable[[HttpRequest], Any]
JsonResponseRequestHandler = Callable[[HttpRequest], JsonResponse]


def json_response(fn: RequestHandler) -> JsonResponseRequestHandler:
    @wraps(fn)
    def wrapper(request: HttpRequest):
        try:
            response_data = fn(request)
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


def require_verified_mail(f: RequestHandler) -> RequestHandler:
    @wraps(f)
    def wrapper(request: HttpRequest):
        if not request.user.is_active:
            return HttpResponseForbidden()

        return f(request)

    return wrapper


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False, blank=False, null=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False, blank=False, null=False)

    class Meta:
        abstract = True
        get_latest_by = "created_at"


@receiver(pre_save, sender=TimestampedModel)
def my_handler(sender, instance: TimestampedModel, **kwargs):
    instance.updated_at = timezone.now()
