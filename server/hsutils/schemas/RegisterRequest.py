import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..json_response import Validatable


@dataclass_json
@dataclass(kw_only=True)
class RegisterRequest(DataClassJsonMixin, Validatable):
    email: str
    password: str
    username: str

    def validate(self):
        if self.email is None:
            raise SchemaValidationError("RegisterRequest.email is null")
        if len(self.email) < 1:
            raise SchemaValidationError("RegisterRequest.email is too short")
        if self.password is None:
            raise SchemaValidationError("RegisterRequest.password is null")
        if len(self.password) < 1:
            raise SchemaValidationError("RegisterRequest.password is too short")
        if self.username is None:
            raise SchemaValidationError("RegisterRequest.username is null")
        if len(self.username) < 1:
            raise SchemaValidationError("RegisterRequest.username is too short")
