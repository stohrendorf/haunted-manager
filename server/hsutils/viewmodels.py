import re
from dataclasses import dataclass
from typing import Callable, List, Optional

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
    announcements: List["AnnouncementEntry"]

    def validate(self):
        validate_announcements_response(self)


@dataclass_json
@dataclass(kw_only=True)
class ChangeEmailRequest:
    email: str

    def validate(self):
        validate_change_email_request(self)


@dataclass_json
@dataclass(kw_only=True)
class ChangePasswordRequest:
    password: str

    def validate(self):
        validate_change_password_request(self)


@dataclass_json
@dataclass(kw_only=True)
class CreateSessionRequest:
    description: str
    tags: List[int]

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
    players: List[str]
    tags: List["SessionTag"]

    def validate(self):
        validate_session(self)


@dataclass_json
@dataclass(kw_only=True)
class SessionAccessRequest:
    api_key: str
    auth_token: str
    session_id: str
    username: str

    def validate(self):
        validate_session_access_request(self)


@dataclass_json
@dataclass(kw_only=True)
class SessionPlayers:
    session_id: str
    usernames: List[str]

    def validate(self):
        validate_session_players(self)


@dataclass_json
@dataclass(kw_only=True)
class SessionTag:
    description: str
    name: str

    def validate(self):
        validate_session_tag(self)


@dataclass_json
@dataclass(kw_only=True)
class SessionsPlayersRequest:
    api_key: str
    sessions: List["SessionPlayers"]

    def validate(self):
        validate_sessions_players_request(self)


@dataclass_json
@dataclass(kw_only=True)
class SessionsResponse:
    sessions: List["Session"]

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
    tags: List["Tag"]

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


def validate_change_email_request(data: ChangeEmailRequest):
    if data.email is None:
        raise SchemaValidationError("ChangeEmailRequest.email")
    if len(data.email) < 1:
        raise SchemaValidationError("ChangeEmailRequest.email")
    return


def validate_change_password_request(data: ChangePasswordRequest):
    if data.password is None:
        raise SchemaValidationError("ChangePasswordRequest.password")
    if len(data.password) < 1:
        raise SchemaValidationError("ChangePasswordRequest.password")
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
    if data.players is None:
        raise SchemaValidationError("Session.players")
    for field_data in data.players:
        if len(field_data) < 1:
            raise SchemaValidationError("Session.players")
    if data.tags is None:
        raise SchemaValidationError("Session.tags")
    for field_data in data.tags:
        validate_session_tag(field_data)
    return


def validate_session_access_request(data: SessionAccessRequest):
    if data.api_key is None:
        raise SchemaValidationError("SessionAccessRequest.api_key")
    if len(data.api_key) < 1:
        raise SchemaValidationError("SessionAccessRequest.api_key")
    if data.auth_token is None:
        raise SchemaValidationError("SessionAccessRequest.auth_token")
    if len(data.auth_token) < 1:
        raise SchemaValidationError("SessionAccessRequest.auth_token")
    if data.session_id is None:
        raise SchemaValidationError("SessionAccessRequest.session_id")
    if len(data.session_id) < 1:
        raise SchemaValidationError("SessionAccessRequest.session_id")
    if data.username is None:
        raise SchemaValidationError("SessionAccessRequest.username")
    if len(data.username) < 1:
        raise SchemaValidationError("SessionAccessRequest.username")
    return


def validate_session_players(data: SessionPlayers):
    if data.session_id is None:
        raise SchemaValidationError("SessionPlayers.session_id")
    if len(data.session_id) < 1:
        raise SchemaValidationError("SessionPlayers.session_id")
    if data.usernames is None:
        raise SchemaValidationError("SessionPlayers.usernames")
    for field_data in data.usernames:
        if len(field_data) < 1:
            raise SchemaValidationError("SessionPlayers.usernames")
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


def validate_sessions_players_request(data: SessionsPlayersRequest):
    if data.api_key is None:
        raise SchemaValidationError("SessionsPlayersRequest.api_key")
    if len(data.api_key) < 1:
        raise SchemaValidationError("SessionsPlayersRequest.api_key")
    if data.sessions is None:
        raise SchemaValidationError("SessionsPlayersRequest.sessions")
    for field_data in data.sessions:
        validate_session_players(field_data)
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
    def wrap(cls, fn: Callable[[HttpRequest], StatsResponse | tuple[int, StatsResponse]]):
        @json_response
        def request_handler(request) -> tuple[int, StatsResponse] | StatsResponse:
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
    def wrap(cls, fn: Callable[[HttpRequest], TagsResponse | tuple[int, TagsResponse]]):
        @json_response
        def request_handler(request) -> tuple[int, TagsResponse] | TagsResponse:
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
    def wrap(cls, fn: Callable[[HttpRequest], SessionsResponse | tuple[int, SessionsResponse]]):
        @json_response
        def request_handler(request) -> tuple[int, SessionsResponse] | SessionsResponse:
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
    def wrap(cls, fn: Callable[[HttpRequest, CreateSessionRequest], SuccessResponse | tuple[int, SuccessResponse]]):
        @json_response
        def request_handler(request) -> tuple[int, SuccessResponse] | SuccessResponse:
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
    def wrap(cls, fn: Callable[[HttpRequest, DeleteSessionRequest], SuccessResponse | tuple[int, SuccessResponse]]):
        @json_response
        def request_handler(request) -> tuple[int, SuccessResponse] | SuccessResponse:
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


class check_session_access:
    path = "api/v0/sessions/check-access"
    operation = "check_session_access"

    @classmethod
    def wrap(cls, fn: Callable[[HttpRequest, SessionAccessRequest], SuccessResponse | tuple[int, SuccessResponse]]):
        @json_response
        def request_handler(request) -> tuple[int, SuccessResponse] | SuccessResponse:
            rq: SessionAccessRequest = SessionAccessRequest.schema().loads(request.body.decode())
            rq.validate()
            response = fn(request, rq)
            if isinstance(response, tuple):
                code, response = response
            else:
                code = HttpResponse.status_code
            response.validate()
            return code, response

        return path(cls.path, request_handler, name=cls.operation)


class update_sessions_players:
    path = "api/v0/sessions/session-players"
    operation = "update_sessions_players"

    @classmethod
    def wrap(cls, fn: Callable[[HttpRequest, SessionsPlayersRequest], Empty | tuple[int, Empty]]):
        @json_response
        def request_handler(request) -> tuple[int, Empty] | Empty:
            rq: SessionsPlayersRequest = SessionsPlayersRequest.schema().loads(request.body.decode())
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
    def wrap(cls, fn: Callable[[HttpRequest], AnnouncementsResponse | tuple[int, AnnouncementsResponse]]):
        @json_response
        def request_handler(request) -> tuple[int, AnnouncementsResponse] | AnnouncementsResponse:
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
    def wrap(cls, fn: Callable[[HttpRequest], ProfileInfoResponse | tuple[int, ProfileInfoResponse]]):
        @json_response
        def request_handler(request) -> tuple[int, ProfileInfoResponse] | ProfileInfoResponse:
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
    def wrap(cls, fn: Callable[[HttpRequest], Empty | tuple[int, Empty]]):
        @json_response
        def request_handler(request) -> tuple[int, Empty] | Empty:
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
    def wrap(cls, fn: Callable[[HttpRequest, LoginRequest], SuccessResponse | tuple[int, SuccessResponse]]):
        @json_response
        def request_handler(request) -> tuple[int, SuccessResponse] | SuccessResponse:
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
    def wrap(cls, fn: Callable[[HttpRequest, RegisterRequest], SuccessResponse | tuple[int, SuccessResponse]]):
        @json_response
        def request_handler(request) -> tuple[int, SuccessResponse] | SuccessResponse:
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


class change_password:
    path = "api/v0/auth/change-password"
    operation = "change_password"

    @classmethod
    def wrap(cls, fn: Callable[[HttpRequest, ChangePasswordRequest], SuccessResponse | tuple[int, SuccessResponse]]):
        @json_response
        def request_handler(request) -> tuple[int, SuccessResponse] | SuccessResponse:
            rq: ChangePasswordRequest = ChangePasswordRequest.schema().loads(request.body.decode())
            rq.validate()
            response = fn(request, rq)
            if isinstance(response, tuple):
                code, response = response
            else:
                code = HttpResponse.status_code
            response.validate()
            return code, response

        return path(cls.path, request_handler, name=cls.operation)


class change_email:
    path = "api/v0/auth/change-email"
    operation = "change_email"

    @classmethod
    def wrap(cls, fn: Callable[[HttpRequest, ChangeEmailRequest], SuccessResponse | tuple[int, SuccessResponse]]):
        @json_response
        def request_handler(request) -> tuple[int, SuccessResponse] | SuccessResponse:
            rq: ChangeEmailRequest = ChangeEmailRequest.schema().loads(request.body.decode())
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
    def wrap(cls, fn: Callable[[HttpRequest], Empty | tuple[int, Empty]]):
        @json_response
        def request_handler(request) -> tuple[int, Empty] | Empty:
            response = fn(request)
            if isinstance(response, tuple):
                code, response = response
            else:
                code = HttpResponse.status_code
            response.validate()
            return code, response

        return path(cls.path, request_handler, name=cls.operation)
