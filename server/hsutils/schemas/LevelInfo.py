import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..json_response import Validatable


@dataclass_json
@dataclass(kw_only=True)
class LevelInfo(DataClassJsonMixin, Validatable):
    id: int
    identifier: str
    title: str

    def validate(self):
        if self.id is None:
            raise SchemaValidationError("LevelInfo.id is null")
        if self.identifier is None:
            raise SchemaValidationError("LevelInfo.identifier is null")
        if len(self.identifier) < 1:
            raise SchemaValidationError("LevelInfo.identifier is too short")
        if self.title is None:
            raise SchemaValidationError("LevelInfo.title is null")
        if len(self.title) < 1:
            raise SchemaValidationError("LevelInfo.title is too short")
