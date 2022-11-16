from http import HTTPStatus
from typing import Optional, TypeVar

from dataclasses_json import DataClassJsonMixin
from django.test import Client

T = TypeVar("T", bound=DataClassJsonMixin)


def get_test_url(client: Client, path: str, response_class: type[T]) -> tuple[HTTPStatus, Optional[T]]:
    r = client.get("/" + path)
    try:
        return HTTPStatus(r.status_code), response_class.schema().loads(r.content.decode())
    except Exception:
        return HTTPStatus(r.status_code), None


def post_test_url(client: Client, path: str, data, response_class: type[T]) -> tuple[HTTPStatus, Optional[T]]:
    r = client.post("/" + path, data=data.schema().dumps(data).encode(), content_type="text/json")
    try:
        return HTTPStatus(r.status_code), response_class.schema().loads(r.content.decode())
    except Exception:
        return HTTPStatus(r.status_code), None
