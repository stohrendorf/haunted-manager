import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json

from ..error import SchemaValidationError
from ..json_response import Validatable


@dataclass_json
@dataclass(kw_only=True)
class SessionAccessRequest(DataClassJsonMixin, Validatable):
    api_key: str
    auth_token: str
    session_id: str
    username: str

    def validate(self):
        if self.api_key is None:
            raise SchemaValidationError("SessionAccessRequest.api_key is null")
        if len(self.api_key) < 1:
            raise SchemaValidationError("SessionAccessRequest.api_key is too short")
        if self.auth_token is None:
            raise SchemaValidationError("SessionAccessRequest.auth_token is null")
        if len(self.auth_token) < 1:
            raise SchemaValidationError("SessionAccessRequest.auth_token is too short")
        if self.session_id is None:
            raise SchemaValidationError("SessionAccessRequest.session_id is null")
        if len(self.session_id) < 1:
            raise SchemaValidationError("SessionAccessRequest.session_id is too short")
        if self.username is None:
            raise SchemaValidationError("SessionAccessRequest.username is null")
        if len(self.username) < 1:
            raise SchemaValidationError("SessionAccessRequest.username is too short")
        return
