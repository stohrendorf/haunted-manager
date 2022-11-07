from typing import Optional, TypeVar

import requests
from dataclasses_json import DataClassJsonMixin
from pytest_django.live_server_helper import LiveServer

T = TypeVar("T", bound=DataClassJsonMixin)


def get_test_url(live_server: LiveServer, path: str, response_class: type[T]) -> tuple[int, Optional[T]]:
    r = requests.get(live_server.url + "/" + path)
    try:
        return r.status_code, response_class.schema().loads(r.text)
    except Exception:
        return r.status_code, None


def post_test_url(live_server: LiveServer, path: str, data, response_class: type[T]) -> tuple[int, Optional[T]]:
    r = requests.post(live_server.url + "/" + path, data=data.schema().dumps(data).encode())
    try:
        return r.status_code, response_class.schema().loads(r.text)
    except Exception:
        return r.status_code, None
