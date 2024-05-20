import re
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.core.files.uploadedfile import UploadedFile

from ..error import SchemaValidationError
from ..validated_response import Validatable
from .Tag import Tag


@dataclass_json
@dataclass(kw_only=True)
class GhostFileResponseEntry(DataClassJsonMixin, Validatable):
    description: str
    downloads: int
    duration: int
    finish_type: str
    id: int
    level_display: str
    level_id: int
    level_identifier: str
    published: bool
    size: int
    tags: List[Tag]
    username: str

    def validate(self):
        if self.description is None:
            raise SchemaValidationError("GhostFileResponseEntry.description is null")
        if self.downloads is None:
            raise SchemaValidationError("GhostFileResponseEntry.downloads is null")
        if self.downloads < 0:
            raise SchemaValidationError("GhostFileResponseEntry.downloads has a value below minimum")
        if self.duration is None:
            raise SchemaValidationError("GhostFileResponseEntry.duration is null")
        if self.duration < 0:
            raise SchemaValidationError("GhostFileResponseEntry.duration has a value below minimum")
        if self.finish_type is None:
            raise SchemaValidationError("GhostFileResponseEntry.finish_type is null")
        if self.id is None:
            raise SchemaValidationError("GhostFileResponseEntry.id is null")
        if self.level_display is None:
            raise SchemaValidationError("GhostFileResponseEntry.level_display is null")
        if len(self.level_display) < 1:
            raise SchemaValidationError("GhostFileResponseEntry.level_display is too short")
        if self.level_id is None:
            raise SchemaValidationError("GhostFileResponseEntry.level_id is null")
        if self.level_identifier is None:
            raise SchemaValidationError("GhostFileResponseEntry.level_identifier is null")
        if len(self.level_identifier) < 1:
            raise SchemaValidationError("GhostFileResponseEntry.level_identifier is too short")
        if self.published is None:
            raise SchemaValidationError("GhostFileResponseEntry.published is null")
        if self.size is None:
            raise SchemaValidationError("GhostFileResponseEntry.size is null")
        if self.size < 0:
            raise SchemaValidationError("GhostFileResponseEntry.size has a value below minimum")
        if self.tags is None:
            raise SchemaValidationError("GhostFileResponseEntry.tags is null")
        for self_tags_entry in self.tags:
            self_tags_entry.validate()
        if self.username is None:
            raise SchemaValidationError("GhostFileResponseEntry.username is null")
        if len(self.username) < 1:
            raise SchemaValidationError("GhostFileResponseEntry.username is too short")
