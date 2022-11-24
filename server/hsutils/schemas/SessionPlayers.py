import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json

from ..error import SchemaValidationError
from ..json_response import Validatable


@dataclass_json
@dataclass(kw_only=True)
class SessionPlayers(DataClassJsonMixin, Validatable):
    session_id: str
    usernames: List[str]

    def validate(self):
        if self.session_id is None:
            raise SchemaValidationError("SessionPlayers.session_id is null")
        if len(self.session_id) < 1:
            raise SchemaValidationError("SessionPlayers.session_id is too short")
        if self.usernames is None:
            raise SchemaValidationError("SessionPlayers.usernames is null")
        for self_usernames_entry in self.usernames:
            if self_usernames_entry is None:
                raise SchemaValidationError("SessionPlayers.usernames is null")
            if len(self_usernames_entry) < 1:
                raise SchemaValidationError("SessionPlayers.usernames is too short")
        return
