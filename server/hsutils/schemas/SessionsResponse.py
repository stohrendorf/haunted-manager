import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..validated_response import Validatable
from .Session import Session


@dataclass_json
@dataclass(kw_only=True)
class SessionsResponse(DataClassJsonMixin, Validatable):
    sessions: List[Session]

    def validate(self):
        if self.sessions is None:
            raise SchemaValidationError("SessionsResponse.sessions is null")
        for self_sessions_entry in self.sessions:
            self_sessions_entry.validate()
