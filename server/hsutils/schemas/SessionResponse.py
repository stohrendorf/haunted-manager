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
class SessionResponse(DataClassJsonMixin, Validatable):
    session: Optional[Session]

    def validate(self):
        if self.session is not None:
            self.session.validate()
