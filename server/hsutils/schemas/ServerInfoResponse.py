import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json

from ..error import SchemaValidationError
from ..json_response import Validatable


@dataclass_json
@dataclass(kw_only=True)
class ServerInfoResponse(DataClassJsonMixin, Validatable):
    coop_url: str
    total_sessions: int
    total_users: int

    def validate(self):
        if self.coop_url is None:
            raise SchemaValidationError("ServerInfoResponse.coop_url is null")
        if len(self.coop_url) < 1:
            raise SchemaValidationError("ServerInfoResponse.coop_url is too short")
        if self.total_sessions is None:
            raise SchemaValidationError("ServerInfoResponse.total_sessions is null")
        if self.total_sessions < 0:
            raise SchemaValidationError("ServerInfoResponse.total_sessions has a value below minimum")
        if self.total_users is None:
            raise SchemaValidationError("ServerInfoResponse.total_users is null")
        if self.total_users < 0:
            raise SchemaValidationError("ServerInfoResponse.total_users has a value below minimum")
        return
