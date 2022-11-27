import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..json_response import Validatable
from .TimeSpan import TimeSpan


@dataclass_json
@dataclass(kw_only=True)
class CreateSessionRequest(DataClassJsonMixin, Validatable):
    description: str
    tags: List[int]
    time: Optional[TimeSpan]

    def validate(self):
        if self.description is None:
            raise SchemaValidationError("CreateSessionRequest.description is null")
        if len(self.description) > 512:
            raise SchemaValidationError("CreateSessionRequest.description is too long")
        if self.tags is None:
            raise SchemaValidationError("CreateSessionRequest.tags is null")
        for self_tags_entry in self.tags:
            if self_tags_entry is None:
                raise SchemaValidationError("CreateSessionRequest.tags is null")
            pass
        if self.time is not None:
            self.time.validate()
