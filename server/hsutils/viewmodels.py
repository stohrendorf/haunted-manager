import re
from dataclasses import dataclass
from typing import Callable, Optional, Union

from dataclasses_json import dataclass_json
from django.http import HttpRequest, HttpResponse
from django.urls import path

from . import json_response


class SchemaValidationError(Exception):
    def __init__(self, path: str):
        super().__init__(path)
        self.path = path

    def __str__(self):
        return f"Schema validation error at {self.path}"


@dataclass_json
@dataclass(kw_only=True)
class AnnouncementEntry:
    background_color: str
    message: str
    text_color: str

    def validate(self):
        validate_announcement_entry(self)


@dataclass_json
@dataclass(kw_only=True)
class AnnouncementsResponse:
    announcements: list["AnnouncementEntry"]

    def validate(self):
        validate_announcements_response(self)


@dataclass_json
@dataclass(kw_only=True)
class CreateSessionRequest:
    description: str
    tags: list[int]

    def validate(self):
        validate_create_session_request(self)


@dataclass_json
@dataclass(kw_only=True)
class DeleteSessionRequest:
    session_id: str

    def validate(self):
        validate_delete_session_request(self)


@dataclass_json
@dataclass(kw_only=True)
class Empty:
    def validate(self):
        validate_empty(self)


@dataclass_json
@dataclass(kw_only=True)
class LoginRequest:
    password: str
    username: str

    def validate(self):
        validate_login_request(self)


@dataclass_json
@dataclass(kw_only=True)
class ProfileInfoResponse:
    auth_token: Optional[str]
    authenticated: bool
    email: Optional[str]
    username: str
    verified: bool

    def validate(self):
        validate_profile_info_response(self)


@dataclass_json
@dataclass(kw_only=True)
class RegisterRequest:
    email: str
    password: str
    username: str

    def validate(self):
        validate_register_request(self)


@dataclass_json
@dataclass(kw_only=True)
class Session:
    description: str
    id: str
    owner: str
    tags: list["SessionTag"]

    def validate(self):
        validate_session(self)


@dataclass_json
@dataclass(kw_only=True)
class SessionTag:
    description: str
    name: str

    def validate(self):
        validate_session_tag(self)


@dataclass_json
@dataclass(kw_only=True)
class SessionsResponse:
    sessions: list["Session"]

    def validate(self):
        validate_sessions_response(self)


@dataclass_json
@dataclass(kw_only=True)
class StatsResponse:
    total_sessions: int
    total_users: int

    def validate(self):
        validate_stats_response(self)


@dataclass_json
@dataclass(kw_only=True)
class SuccessResponse:
    message: str
    success: bool

    def validate(self):
        validate_success_response(self)


@dataclass_json
@dataclass(kw_only=True)
class Tag:
    description: str
    id: int
    name: str

    def validate(self):
        validate_tag(self)


@dataclass_json
@dataclass(kw_only=True)
class TagsResponse:
    tags: list["Tag"]

    def validate(self):
        validate_tags_response(self)


def validate_announcement_entry(data: AnnouncementEntry):
    if data.background_color is None:
        raise SchemaValidationError("AnnouncementEntry.background_color")
    if len(data.background_color) < 1:
        raise SchemaValidationError("AnnouncementEntry.background_color")
    if data.message is None:
        raise SchemaValidationError("AnnouncementEntry.message")
    if len(data.message) < 1:
        raise SchemaValidationError("AnnouncementEntry.message")
    if data.text_color is None:
        raise SchemaValidationError("AnnouncementEntry.text_color")
    if len(data.text_color) < 1:
        raise SchemaValidationError("AnnouncementEntry.text_color")
    return


def validate_announcements_response(data: AnnouncementsResponse):
    if data.announcements is None:
        raise SchemaValidationError("AnnouncementsResponse.announcements")
    for field_data in data.announcements:
        validate_announcement_entry(field_data)
    return


def validate_create_session_request(data: CreateSessionRequest):
    if data.description is None:
        raise SchemaValidationError("CreateSessionRequest.description")
    if data.tags is None:
        raise SchemaValidationError("CreateSessionRequest.tags")
    for field_data in data.tags:
        pass
    return


def validate_delete_session_request(data: DeleteSessionRequest):
    if data.session_id is None:
        raise SchemaValidationError("DeleteSessionRequest.session_id")
    if len(data.session_id) < 1:
        raise SchemaValidationError("DeleteSessionRequest.session_id")
    return


def validate_empty(data: Empty):
    return


def validate_login_request(data: LoginRequest):
    if data.password is None:
        raise SchemaValidationError("LoginRequest.password")
    if len(data.password) < 1:
        raise SchemaValidationError("LoginRequest.password")
    if data.username is None:
        raise SchemaValidationError("LoginRequest.username")
    if len(data.username) < 1:
        raise SchemaValidationError("LoginRequest.username")
    return


def validate_profile_info_response(data: ProfileInfoResponse):
    if data.auth_token is not None:
        if len(data.auth_token) < 1:
            raise SchemaValidationError("ProfileInfoResponse.auth_token")
    if data.authenticated is None:
        raise SchemaValidationError("ProfileInfoResponse.authenticated")
    if data.email is not None:
        if len(data.email) < 1:
            raise SchemaValidationError("ProfileInfoResponse.email")
    if data.username is None:
        raise SchemaValidationError("ProfileInfoResponse.username")
    if len(data.username) < 1:
        raise SchemaValidationError("ProfileInfoResponse.username")
    if data.verified is None:
        raise SchemaValidationError("ProfileInfoResponse.verified")
    return


def validate_register_request(data: RegisterRequest):
    if data.email is None:
        raise SchemaValidationError("RegisterRequest.email")
    if len(data.email) < 1:
        raise SchemaValidationError("RegisterRequest.email")
    if data.password is None:
        raise SchemaValidationError("RegisterRequest.password")
    if len(data.password) < 1:
        raise SchemaValidationError("RegisterRequest.password")
    if data.username is None:
        raise SchemaValidationError("RegisterRequest.username")
    if len(data.username) < 1:
        raise SchemaValidationError("RegisterRequest.username")
    return


def validate_session(data: Session):
    if data.description is None:
        raise SchemaValidationError("Session.description")
    if data.id is None:
        raise SchemaValidationError("Session.id")
    if len(data.id) < 1:
        raise SchemaValidationError("Session.id")
    if data.owner is None:
        raise SchemaValidationError("Session.owner")
    if len(data.owner) < 1:
        raise SchemaValidationError("Session.owner")
    if data.tags is None:
        raise SchemaValidationError("Session.tags")
    for field_data in data.tags:
        validate_session_tag(field_data)
    return


def validate_session_tag(data: SessionTag):
    if data.description is None:
        raise SchemaValidationError("SessionTag.description")
    if len(data.description) < 1:
        raise SchemaValidationError("SessionTag.description")
    if data.name is None:
        raise SchemaValidationError("SessionTag.name")
    if len(data.name) < 1:
        raise SchemaValidationError("SessionTag.name")
    return


def validate_sessions_response(data: SessionsResponse):
    if data.sessions is None:
        raise SchemaValidationError("SessionsResponse.sessions")
    for field_data in data.sessions:
        validate_session(field_data)
    return


def validate_stats_response(data: StatsResponse):
    if data.total_sessions is None:
        raise SchemaValidationError("StatsResponse.total_sessions")
    if data.total_sessions < 0:
        raise SchemaValidationError("StatsResponse.total_sessions")
    if data.total_users is None:
        raise SchemaValidationError("StatsResponse.total_users")
    if data.total_users < 0:
        raise SchemaValidationError("StatsResponse.total_users")
    return


def validate_success_response(data: SuccessResponse):
    if data.message is None:
        raise SchemaValidationError("SuccessResponse.message")
    if data.success is None:
        raise SchemaValidationError("SuccessResponse.success")
    return


def validate_tag(data: Tag):
    if data.description is None:
        raise SchemaValidationError("Tag.description")
    if data.id is None:
        raise SchemaValidationError("Tag.id")
    if data.name is None:
        raise SchemaValidationError("Tag.name")
    if len(data.name) < 1:
        raise SchemaValidationError("Tag.name")
    return


def validate_tags_response(data: TagsResponse):
    if data.tags is None:
        raise SchemaValidationError("TagsResponse.tags")
    for field_data in data.tags:
        validate_tag(field_data)
    return


class get_stats:
    path = "api/v0/stats"
    operation = "get_stats"

    @classmethod
    def wrap(cls, fn: Callable[[HttpRequest], StatsResponse]):
        @json_response
        def request_handler(request) -> Union[tuple[int, StatsResponse], StatsResponse]:
            response = fn(request)
            if isinstance(response, tuple):
                code, response = response
            else:
                code = HttpResponse.status_code
            response.validate()
            return code, response

        return path(cls.path, request_handler, name=cls.operation)


class get_tags:
    path = "api/v0/tags"
    operation = "get_tags"

    @classmethod
    def wrap(cls, fn: Callable[[HttpRequest], TagsResponse]):
        @json_response
        def request_handler(request) -> Union[tuple[int, TagsResponse], TagsResponse]:
            response = fn(request)
            if isinstance(response, tuple):
                code, response = response
            else:
                code = HttpResponse.status_code
            response.validate()
            return code, response

        return path(cls.path, request_handler, name=cls.operation)


class get_sessions:
    path = "api/v0/sessions"
    operation = "get_sessions"

    @classmethod
    def wrap(cls, fn: Callable[[HttpRequest], SessionsResponse]):
        @json_response
        def request_handler(request) -> Union[tuple[int, SessionsResponse], SessionsResponse]:
            response = fn(request)
            if isinstance(response, tuple):
                code, response = response
            else:
                code = HttpResponse.status_code
            response.validate()
            return code, response

        return path(cls.path, request_handler, name=cls.operation)


class create_session:
    path = "api/v0/sessions/create"
    operation = "create_session"

    @classmethod
    def wrap(cls, fn: Callable[[HttpRequest, CreateSessionRequest], SuccessResponse]):
        @json_response
        def request_handler(request) -> Union[tuple[int, SuccessResponse], SuccessResponse]:
            rq: CreateSessionRequest = CreateSessionRequest.schema().loads(request.body.decode())
            rq.validate()
            response = fn(request, rq)
            if isinstance(response, tuple):
                code, response = response
            else:
                code = HttpResponse.status_code
            response.validate()
            return code, response

        return path(cls.path, request_handler, name=cls.operation)


class delete_session:
    path = "api/v0/sessions/delete"
    operation = "delete_session"

    @classmethod
    def wrap(cls, fn: Callable[[HttpRequest, DeleteSessionRequest], SuccessResponse]):
        @json_response
        def request_handler(request) -> Union[tuple[int, SuccessResponse], SuccessResponse]:
            rq: DeleteSessionRequest = DeleteSessionRequest.schema().loads(request.body.decode())
            rq.validate()
            response = fn(request, rq)
            if isinstance(response, tuple):
                code, response = response
            else:
                code = HttpResponse.status_code
            response.validate()
            return code, response

        return path(cls.path, request_handler, name=cls.operation)


class get_announcements:
    path = "api/v0/announcements"
    operation = "get_announcements"

    @classmethod
    def wrap(cls, fn: Callable[[HttpRequest], AnnouncementsResponse]):
        @json_response
        def request_handler(request) -> Union[tuple[int, AnnouncementsResponse], AnnouncementsResponse]:
            response = fn(request)
            if isinstance(response, tuple):
                code, response = response
            else:
                code = HttpResponse.status_code
            response.validate()
            return code, response

        return path(cls.path, request_handler, name=cls.operation)


class get_profile:
    path = "api/v0/auth/profile"
    operation = "get_profile"

    @classmethod
    def wrap(cls, fn: Callable[[HttpRequest], ProfileInfoResponse]):
        @json_response
        def request_handler(request) -> Union[tuple[int, ProfileInfoResponse], ProfileInfoResponse]:
            response = fn(request)
            if isinstance(response, tuple):
                code, response = response
            else:
                code = HttpResponse.status_code
            response.validate()
            return code, response

        return path(cls.path, request_handler, name=cls.operation)


class regenerate_token:
    path = "api/v0/auth/regenerate-token"
    operation = "regenerate_token"

    @classmethod
    def wrap(cls, fn: Callable[[HttpRequest], Empty]):
        @json_response
        def request_handler(request) -> Union[tuple[int, Empty], Empty]:
            response = fn(request)
            if isinstance(response, tuple):
                code, response = response
            else:
                code = HttpResponse.status_code
            response.validate()
            return code, response

        return path(cls.path, request_handler, name=cls.operation)


class login:
    path = "api/v0/auth/login"
    operation = "login"

    @classmethod
    def wrap(cls, fn: Callable[[HttpRequest, LoginRequest], SuccessResponse]):
        @json_response
        def request_handler(request) -> Union[tuple[int, SuccessResponse], SuccessResponse]:
            rq: LoginRequest = LoginRequest.schema().loads(request.body.decode())
            rq.validate()
            response = fn(request, rq)
            if isinstance(response, tuple):
                code, response = response
            else:
                code = HttpResponse.status_code
            response.validate()
            return code, response

        return path(cls.path, request_handler, name=cls.operation)


class register:
    path = "api/v0/auth/register"
    operation = "register"

    @classmethod
    def wrap(cls, fn: Callable[[HttpRequest, RegisterRequest], SuccessResponse]):
        @json_response
        def request_handler(request) -> Union[tuple[int, SuccessResponse], SuccessResponse]:
            rq: RegisterRequest = RegisterRequest.schema().loads(request.body.decode())
            rq.validate()
            response = fn(request, rq)
            if isinstance(response, tuple):
                code, response = response
            else:
                code = HttpResponse.status_code
            response.validate()
            return code, response

        return path(cls.path, request_handler, name=cls.operation)


class logout:
    path = "api/v0/auth/logout"
    operation = "logout"

    @classmethod
    def wrap(cls, fn: Callable[[HttpRequest], Empty]):
        @json_response
        def request_handler(request) -> Union[tuple[int, Empty], Empty]:
            response = fn(request)
            if isinstance(response, tuple):
                code, response = response
            else:
                code = HttpResponse.status_code
            response.validate()
            return code, response

        return path(cls.path, request_handler, name=cls.operation)
