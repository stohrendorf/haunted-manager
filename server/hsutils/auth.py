from functools import wraps
from http import HTTPStatus
from typing import Callable, Concatenate, ParamSpec, TypeVar

from django.http import HttpRequest

P = ParamSpec("P")
T = TypeVar("T")


def require_authenticated(
    response: T,
    status: HTTPStatus = HTTPStatus.UNAUTHORIZED,
) -> Callable[[Callable[[Concatenate[HttpRequest, P]], T]], Callable[Concatenate[HttpRequest, P], T | tuple[int, T]]]:
    def decorator(handler: Callable[[Concatenate[HttpRequest, P]], T]):
        @wraps(handler)
        def wrapper(request: HttpRequest, *args: P.args, **kwargs: P.kwargs) -> T | tuple[int, T]:
            if not request.user.is_active or not request.user.is_authenticated:
                return status, response
            return handler(request, *args, **kwargs)

        return wrapper

    return decorator
