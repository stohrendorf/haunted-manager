import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..validated_response import Validatable
from .SessionPlayers import SessionPlayers


@dataclass_json
@dataclass(kw_only=True)
class SessionsPlayersRequest(DataClassJsonMixin, Validatable):
    api_key: str
    sessions: List[SessionPlayers]

    def validate(self):
        if self.api_key is None:
            raise SchemaValidationError("SessionsPlayersRequest.api_key is null")
        if len(self.api_key) < 1:
            raise SchemaValidationError("SessionsPlayersRequest.api_key is too short")
        if self.sessions is None:
            raise SchemaValidationError("SessionsPlayersRequest.sessions is null")
        for self_sessions_entry in self.sessions:
            self_sessions_entry.validate()
