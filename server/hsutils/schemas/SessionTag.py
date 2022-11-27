import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..json_response import Validatable


@dataclass_json
@dataclass(kw_only=True)
class SessionTag(DataClassJsonMixin, Validatable):
    description: str
    name: str

    def validate(self):
        if self.description is None:
            raise SchemaValidationError("SessionTag.description is null")
        if len(self.description) < 1:
            raise SchemaValidationError("SessionTag.description is too short")
        if self.name is None:
            raise SchemaValidationError("SessionTag.name is null")
        if len(self.name) < 1:
            raise SchemaValidationError("SessionTag.name is too short")
