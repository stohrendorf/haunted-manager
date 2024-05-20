import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..validated_response import Validatable


@dataclass_json
@dataclass(kw_only=True)
class SuccessResponse(DataClassJsonMixin, Validatable):
    message: str
    success: bool

    def validate(self):
        if self.message is None:
            raise SchemaValidationError("SuccessResponse.message is null")
        if self.success is None:
            raise SchemaValidationError("SuccessResponse.success is null")
        return
