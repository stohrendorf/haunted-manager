import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..json_response import Validatable
from .SessionTag import SessionTag
from .TimeSpan import TimeSpan


@dataclass_json
@dataclass(kw_only=True)
class Session(DataClassJsonMixin, Validatable):
    description: str
    id: str
    owner: str
    players: List[str]
    private: bool
    tags: List[SessionTag]
    time: Optional[TimeSpan]

    def validate(self):
        if self.description is None:
            raise SchemaValidationError("Session.description is null")
        if self.id is None:
            raise SchemaValidationError("Session.id is null")
        if len(self.id) < 1:
            raise SchemaValidationError("Session.id is too short")
        if self.owner is None:
            raise SchemaValidationError("Session.owner is null")
        if len(self.owner) < 1:
            raise SchemaValidationError("Session.owner is too short")
        if self.players is None:
            raise SchemaValidationError("Session.players is null")
        for self_players_entry in self.players:
            if self_players_entry is None:
                raise SchemaValidationError("Session.players is null")
            if len(self_players_entry) < 1:
                raise SchemaValidationError("Session.players is too short")
        if self.private is None:
            raise SchemaValidationError("Session.private is null")
        if self.tags is None:
            raise SchemaValidationError("Session.tags is null")
        for self_tags_entry in self.tags:
            self_tags_entry.validate()
        if self.time is not None:
            self.time.validate()
