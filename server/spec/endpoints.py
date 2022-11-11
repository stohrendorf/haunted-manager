import re
from dataclasses import dataclass
from enum import Enum, unique
from typing import Optional

from structural import BaseField, Compound, gather_dependencies


@unique
class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"


@dataclass
class Endpoint:
    operation_name: str
    response: Compound
    body: Optional[Compound] = None


def gather_compounds(endpoints: dict[str, dict[HttpMethod, Endpoint]]) -> list[type[BaseField | Compound]]:
    if len(
        {endpoint.operation_name for endpoints_methods in endpoints.values() for endpoint in endpoints_methods.values()}
    ) != len(endpoints):
        raise RuntimeError("operation names must be unique")

    all_compounds: set[type[BaseField | Compound]] = set()
    for endpoints_methods in endpoints.values():
        for endpoint in endpoints_methods.values():
            all_compounds |= gather_dependencies(type(endpoint.response))
            if endpoint.body is not None:
                all_compounds |= gather_dependencies(type(endpoint.body))
    return sorted(all_compounds, key=lambda x: x.typename())


_URL_PARAM_PATTERN = re.compile(r"<(?P<type>[^:]+):(?P<name>[^>]+)>")


@dataclass(kw_only=True)
class UrlParam:
    type: str
    span: tuple[int, int]


def get_url_params(url: str) -> dict[str, UrlParam]:
    search_start = 0
    params = dict()
    while match := _URL_PARAM_PATTERN.search(url, pos=search_start):
        params[match.group("name")] = UrlParam(
            type=match.group("type"),
            span=match.span(),
        )
        search_start = match.end()
    return params
