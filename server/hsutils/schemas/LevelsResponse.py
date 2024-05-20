import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..validated_response import Validatable
from .LevelInfo import LevelInfo


@dataclass_json
@dataclass(kw_only=True)
class LevelsResponse(DataClassJsonMixin, Validatable):
    levels: List[LevelInfo]

    def validate(self):
        if self.levels is None:
            raise SchemaValidationError("LevelsResponse.levels is null")
        for self_levels_entry in self.levels:
            self_levels_entry.validate()
