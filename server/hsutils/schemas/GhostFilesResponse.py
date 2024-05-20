import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..validated_response import Validatable
from .GhostFileResponseEntry import GhostFileResponseEntry


@dataclass_json
@dataclass(kw_only=True)
class GhostFilesResponse(DataClassJsonMixin, Validatable):
    files: List[GhostFileResponseEntry]

    def validate(self):
        if self.files is None:
            raise SchemaValidationError("GhostFilesResponse.files is null")
        for self_files_entry in self.files:
            self_files_entry.validate()
