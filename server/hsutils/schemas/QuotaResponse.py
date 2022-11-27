import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..json_response import Validatable


@dataclass_json
@dataclass(kw_only=True)
class QuotaResponse(DataClassJsonMixin, Validatable):
    current: int
    max: int

    def validate(self):
        if self.current is None:
            raise SchemaValidationError("QuotaResponse.current is null")
        if self.current < 0:
            raise SchemaValidationError("QuotaResponse.current has a value below minimum")
        if self.max is None:
            raise SchemaValidationError("QuotaResponse.max is null")
        if self.max < 0:
            raise SchemaValidationError("QuotaResponse.max has a value below minimum")
