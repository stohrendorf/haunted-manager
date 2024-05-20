import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..validated_response import Validatable


@dataclass_json
@dataclass(kw_only=True)
class ChangeUsernameRequest(DataClassJsonMixin, Validatable):
    username: str

    def validate(self):
        if self.username is None:
            raise SchemaValidationError("ChangeUsernameRequest.username is null")
        if len(self.username) < 1:
            raise SchemaValidationError("ChangeUsernameRequest.username is too short")
