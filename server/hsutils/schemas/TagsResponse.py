import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..json_response import Validatable
from .Tag import Tag


@dataclass_json
@dataclass(kw_only=True)
class TagsResponse(DataClassJsonMixin, Validatable):
    tags: List[Tag]

    def validate(self):
        if self.tags is None:
            raise SchemaValidationError("TagsResponse.tags is null")
        for self_tags_entry in self.tags:
            self_tags_entry.validate()
