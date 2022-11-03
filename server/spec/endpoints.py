from dataclasses import dataclass
from typing import Optional

from structural import BaseField, Compound, gather_dependencies


@dataclass
class Endpoint:
    operation_name: str
    path: str
    method: str
    response: Compound
    body: Optional[Compound] = None


def gather_compounds(*endpoints: Endpoint) -> list[type[BaseField | Compound]]:
    if len({ep.operation_name for ep in endpoints}) != len(endpoints):
        raise RuntimeError("operation names must be unique")
    if len({ep.path for ep in endpoints}) != len(endpoints):
        raise RuntimeError("paths must be unique")

    all_compounds: set[type[BaseField | Compound]] = set()
    for endpoint in endpoints:
        all_compounds |= gather_dependencies(type(endpoint.response))
        if endpoint.body is not None:
            all_compounds |= gather_dependencies(type(endpoint.body))
    return sorted(all_compounds, key=lambda x: x.typename())
