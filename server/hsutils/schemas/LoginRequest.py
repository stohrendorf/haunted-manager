import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json

from ..error import SchemaValidationError
from ..json_response import Validatable


@dataclass_json
@dataclass(kw_only=True)
class LoginRequest(DataClassJsonMixin, Validatable):
    password: str
    username: str

    def validate(self):
        if self.password is None:
            raise SchemaValidationError("LoginRequest.password is null")
        if len(self.password) < 1:
            raise SchemaValidationError("LoginRequest.password is too short")
        if self.username is None:
            raise SchemaValidationError("LoginRequest.username is null")
        if len(self.username) < 1:
            raise SchemaValidationError("LoginRequest.username is too short")
        return
