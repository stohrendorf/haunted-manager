from functools import wraps
from typing import Any, Callable

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

RequestHandler = Callable[[HttpRequest], HttpResponse]
HttpResponseRequestHandler = Callable[[HttpRequest], Any]
JsonResponseRequestHandler = Callable[[HttpRequest], JsonResponse]


def json_response(f: RequestHandler) -> JsonResponseRequestHandler:
    @wraps(f)
    def wrapper(request: HttpRequest):
        try:
            response_data = f(request)
        except Exception as e:
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


@receiver(pre_save, sender=TimestampedModel)
def my_handler(sender, instance: TimestampedModel, **kwargs):
    instance.updated_at = timezone.now()
