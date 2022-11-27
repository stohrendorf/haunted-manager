import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..json_response import Validatable
from .AnnouncementEntry import AnnouncementEntry


@dataclass_json
@dataclass(kw_only=True)
class AnnouncementsResponse(DataClassJsonMixin, Validatable):
    announcements: List[AnnouncementEntry]

    def validate(self):
        if self.announcements is None:
            raise SchemaValidationError("AnnouncementsResponse.announcements is null")
        for self_announcements_entry in self.announcements:
            self_announcements_entry.validate()
