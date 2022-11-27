import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..json_response import Validatable
from .GhostFileResponseEntry import GhostFileResponseEntry


@dataclass_json
@dataclass(kw_only=True)
class GhostFileResponse(DataClassJsonMixin, Validatable):
    ghost: Optional[GhostFileResponseEntry]

    def validate(self):
        if self.ghost is not None:
            self.ghost.validate()
