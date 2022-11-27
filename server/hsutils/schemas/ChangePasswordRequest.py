import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..json_response import Validatable


@dataclass_json
@dataclass(kw_only=True)
class ChangePasswordRequest(DataClassJsonMixin, Validatable):
    password: str

    def validate(self):
        if self.password is None:
            raise SchemaValidationError("ChangePasswordRequest.password is null")
        if len(self.password) < 1:
            raise SchemaValidationError("ChangePasswordRequest.password is too short")
