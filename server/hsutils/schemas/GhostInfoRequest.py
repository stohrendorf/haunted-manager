import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..json_response import Validatable


@dataclass_json
@dataclass(kw_only=True)
class GhostInfoRequest(DataClassJsonMixin, Validatable):
    description: str
    published: bool
    tags: List[int]

    def validate(self):
        if self.description is None:
            raise SchemaValidationError("GhostInfoRequest.description is null")
        if self.published is None:
            raise SchemaValidationError("GhostInfoRequest.published is null")
        if self.tags is None:
            raise SchemaValidationError("GhostInfoRequest.tags is null")
        for self_tags_entry in self.tags:
            if self_tags_entry is None:
                raise SchemaValidationError("GhostInfoRequest.tags is null")
            pass
