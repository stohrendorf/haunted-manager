import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..json_response import Validatable


@dataclass_json
@dataclass(kw_only=True)
class Tag(DataClassJsonMixin, Validatable):
    description: str
    id: int
    name: str

    def validate(self):
        if self.description is None:
            raise SchemaValidationError("Tag.description is null")
        if self.id is None:
            raise SchemaValidationError("Tag.id is null")
        if self.name is None:
            raise SchemaValidationError("Tag.name is null")
        if len(self.name) < 1:
            raise SchemaValidationError("Tag.name is too short")
