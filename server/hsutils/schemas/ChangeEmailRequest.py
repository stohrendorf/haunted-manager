import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..validated_response import Validatable


@dataclass_json
@dataclass(kw_only=True)
class ChangeEmailRequest(DataClassJsonMixin, Validatable):
    email: str

    def validate(self):
        if self.email is None:
            raise SchemaValidationError("ChangeEmailRequest.email is null")
        if len(self.email) < 1:
            raise SchemaValidationError("ChangeEmailRequest.email is too short")
