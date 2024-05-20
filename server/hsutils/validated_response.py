import logging
from functools import wraps
from typing import Callable, Concatenate, ParamSpec, TypeVar

from dataclasses_json import DataClassJsonMixin
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBase,
    HttpResponseServerError,
    JsonResponse,
)


class Validatable:
    def validate(self):
        raise NotImplementedError


T = TypeVar("T", DataClassJsonMixin, Validatable, HttpResponseBase, covariant=True)
P = ParamSpec("P")


def validated_response(
    handler: Callable[Concatenate[HttpRequest, P], HttpResponseBase | T | tuple[int, T]],
) -> Callable[Concatenate[HttpRequest, P], HttpResponseBase]:
    @wraps(handler)
    def wrapper(request: HttpRequest, *args: P.args, **kwargs: P.kwargs) -> HttpResponseBase:
        try:
            response_data = handler(request, *args, **kwargs)
            if isinstance(response_data, HttpResponseBase):
                return response_data

            response_code = HttpResponse.status_code
            if isinstance(response_data, tuple):
                response_code, response_data = response_data
                assert not isinstance(
                    response_data, HttpResponseBase
                ), "HttpResponseBase must not provide a status code"

            assert isinstance(response_data, Validatable)
            response_data.validate()

            return JsonResponse(
                data=response_data.to_dict(),
                status=response_code,
            )
        except Exception:
            logging.error("request processing error", exc_info=True)
            return JsonResponse(
                data={},
                status=HttpResponseServerError.status_code,
            )

    return wrapper
