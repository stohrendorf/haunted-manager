import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..json_response import Validatable


@dataclass_json
@dataclass(kw_only=True)
class AnnouncementEntry(DataClassJsonMixin, Validatable):
    background_color: str
    message: str
    text_color: str

    def validate(self):
        if self.background_color is None:
            raise SchemaValidationError("AnnouncementEntry.background_color is null")
        if len(self.background_color) < 1:
            raise SchemaValidationError("AnnouncementEntry.background_color is too short")
        if self.message is None:
            raise SchemaValidationError("AnnouncementEntry.message is null")
        if len(self.message) < 1:
            raise SchemaValidationError("AnnouncementEntry.message is too short")
        if self.text_color is None:
            raise SchemaValidationError("AnnouncementEntry.text_color is null")
        if len(self.text_color) < 1:
            raise SchemaValidationError("AnnouncementEntry.text_color is too short")
