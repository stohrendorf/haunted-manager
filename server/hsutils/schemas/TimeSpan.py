import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..validated_response import Validatable


@dataclass_json
@dataclass(kw_only=True)
class TimeSpan(DataClassJsonMixin, Validatable):
    end: str
    start: str

    def validate(self):
        if self.end is None:
            raise SchemaValidationError("TimeSpan.end is null")
        if not re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?(\+[0-9]{2}:[0-9]{2}|Z)", self.end
        ):
            raise SchemaValidationError("TimeSpan.end has an invalid format")
        if self.start is None:
            raise SchemaValidationError("TimeSpan.start is null")
        if not re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?(\+[0-9]{2}:[0-9]{2}|Z)", self.start
        ):
            raise SchemaValidationError("TimeSpan.start has an invalid format")
