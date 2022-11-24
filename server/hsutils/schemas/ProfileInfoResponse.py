import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json

from ..error import SchemaValidationError
from ..json_response import Validatable


@dataclass_json
@dataclass(kw_only=True)
class ProfileInfoResponse(DataClassJsonMixin, Validatable):
    auth_token: Optional[str]
    authenticated: bool
    email: Optional[str]
    is_staff: bool
    username: str
    verified: bool

    def validate(self):
        if self.auth_token is not None:
            if len(self.auth_token) < 1:
                raise SchemaValidationError("ProfileInfoResponse.auth_token is too short")
        if self.authenticated is None:
            raise SchemaValidationError("ProfileInfoResponse.authenticated is null")
        if self.email is not None:
            if len(self.email) < 1:
                raise SchemaValidationError("ProfileInfoResponse.email is too short")
        if self.is_staff is None:
            raise SchemaValidationError("ProfileInfoResponse.is_staff is null")
        if self.username is None:
            raise SchemaValidationError("ProfileInfoResponse.username is null")
        if len(self.username) < 1:
            raise SchemaValidationError("ProfileInfoResponse.username is too short")
        if self.verified is None:
            raise SchemaValidationError("ProfileInfoResponse.verified is null")
        return
