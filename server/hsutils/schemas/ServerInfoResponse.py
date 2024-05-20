import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..validated_response import Validatable


@dataclass_json
@dataclass(kw_only=True)
class ServerInfoResponse(DataClassJsonMixin, Validatable):
    coop_url: str
    total_ghost_duration: int
    total_ghosts: int
    total_sessions: int
    total_users: int

    def validate(self):
        if self.coop_url is None:
            raise SchemaValidationError("ServerInfoResponse.coop_url is null")
        if len(self.coop_url) < 1:
            raise SchemaValidationError("ServerInfoResponse.coop_url is too short")
        if self.total_ghost_duration is None:
            raise SchemaValidationError("ServerInfoResponse.total_ghost_duration is null")
        if self.total_ghost_duration < 0:
            raise SchemaValidationError("ServerInfoResponse.total_ghost_duration has a value below minimum")
        if self.total_ghosts is None:
            raise SchemaValidationError("ServerInfoResponse.total_ghosts is null")
        if self.total_ghosts < 0:
            raise SchemaValidationError("ServerInfoResponse.total_ghosts has a value below minimum")
        if self.total_sessions is None:
            raise SchemaValidationError("ServerInfoResponse.total_sessions is null")
        if self.total_sessions < 0:
            raise SchemaValidationError("ServerInfoResponse.total_sessions has a value below minimum")
        if self.total_users is None:
            raise SchemaValidationError("ServerInfoResponse.total_users is null")
        if self.total_users < 0:
            raise SchemaValidationError("ServerInfoResponse.total_users has a value below minimum")
