import re
from dataclasses import dataclass
from enum import Enum
from typing import Callable, List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.http import HttpRequest, HttpResponse
from django.urls import path

from . import json_response


class SchemaValidationError(Exception):
    def __init__(self, path: str):
        super().__init__(path)
        self.path = path

    def __str__(self):
        return f"Schema validation error at {self.path}"


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"


@dataclass_json
@dataclass(kw_only=True)
class AnnouncementEntry(DataClassJsonMixin):
    background_color: str
    message: str
    text_color: str

    def validate(self):
        validate_announcement_entry(self)


@dataclass_json
@dataclass(kw_only=True)
class AnnouncementsResponse(DataClassJsonMixin):
    announcements: List["AnnouncementEntry"]

    def validate(self):
        validate_announcements_response(self)


@dataclass_json
@dataclass(kw_only=True)
class ChangeEmailRequest(DataClassJsonMixin):
    email: str

    def validate(self):
        validate_change_email_request(self)


@dataclass_json
@dataclass(kw_only=True)
class ChangePasswordRequest(DataClassJsonMixin):
    password: str

    def validate(self):
        validate_change_password_request(self)


@dataclass_json
@dataclass(kw_only=True)
class ChangeUsernameRequest(DataClassJsonMixin):
    username: str

    def validate(self):
        validate_change_username_request(self)


@dataclass_json
@dataclass(kw_only=True)
class CreateSessionRequest(DataClassJsonMixin):
    description: str
    tags: List[int]

    def validate(self):
        validate_create_session_request(self)


@dataclass_json
@dataclass(kw_only=True)
class DeleteSessionRequest(DataClassJsonMixin):
    session_id: str

    def validate(self):
        validate_delete_session_request(self)


@dataclass_json
@dataclass(kw_only=True)
class Empty(DataClassJsonMixin):
    def validate(self):
        validate_empty(self)


@dataclass_json
@dataclass(kw_only=True)
class LoginRequest(DataClassJsonMixin):
    password: str
    username: str

    def validate(self):
        validate_login_request(self)


@dataclass_json
@dataclass(kw_only=True)
class ProfileInfoResponse(DataClassJsonMixin):
    auth_token: Optional[str]
    authenticated: bool
    email: Optional[str]
    username: str
    verified: bool

    def validate(self):
        validate_profile_info_response(self)


@dataclass_json
@dataclass(kw_only=True)
class RegisterRequest(DataClassJsonMixin):
    email: str
    password: str
    username: str

    def validate(self):
        validate_register_request(self)


@dataclass_json
@dataclass(kw_only=True)
class ServerInfoResponse(DataClassJsonMixin):
    coop_url: str
    total_sessions: int
    total_users: int

    def validate(self):
        validate_server_info_response(self)


@dataclass_json
@dataclass(kw_only=True)
class Session(DataClassJsonMixin):
    description: str
    id: str
    owner: str
    players: List[str]
    tags: List["SessionTag"]

    def validate(self):
        validate_session(self)


@dataclass_json
@dataclass(kw_only=True)
class SessionAccessRequest(DataClassJsonMixin):
    api_key: str
    auth_token: str
    session_id: str
    username: str

    def validate(self):
        validate_session_access_request(self)


@dataclass_json
@dataclass(kw_only=True)
class SessionPlayers(DataClassJsonMixin):
    session_id: str
    usernames: List[str]

    def validate(self):
        validate_session_players(self)


@dataclass_json
@dataclass(kw_only=True)
class SessionResponse(DataClassJsonMixin):
    session: Optional["Session"]

    def validate(self):
        validate_session_response(self)


@dataclass_json
@dataclass(kw_only=True)
class SessionTag(DataClassJsonMixin):
    description: str
    name: str

    def validate(self):
        validate_session_tag(self)


@dataclass_json
@dataclass(kw_only=True)
class SessionsPlayersRequest(DataClassJsonMixin):
    api_key: str
    sessions: List["SessionPlayers"]

    def validate(self):
        validate_sessions_players_request(self)


@dataclass_json
@dataclass(kw_only=True)
class SessionsResponse(DataClassJsonMixin):
    sessions: List["Session"]

    def validate(self):
        validate_sessions_response(self)


@dataclass_json
@dataclass(kw_only=True)
class SuccessResponse(DataClassJsonMixin):
    message: str
    success: bool

    def validate(self):
        validate_success_response(self)


@dataclass_json
@dataclass(kw_only=True)
class Tag(DataClassJsonMixin):
    description: str
    id: int
    name: str

    def validate(self):
        validate_tag(self)


@dataclass_json
@dataclass(kw_only=True)
class TagsResponse(DataClassJsonMixin):
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


def validate_change_username_request(data: ChangeUsernameRequest):
    if data.username is None:
        raise SchemaValidationError("ChangeUsernameRequest.username")
    if len(data.username) < 1:
        raise SchemaValidationError("ChangeUsernameRequest.username")
    return


def validate_create_session_request(data: CreateSessionRequest):
    if data.description is None:
        raise SchemaValidationError("CreateSessionRequest.description")
    if data.tags is None:
        raise SchemaValidationError("CreateSessionRequest.tags")
    for field_data in data.tags:
        if field_data is None:
            raise SchemaValidationError("CreateSessionRequest.tags")
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


def validate_server_info_response(data: ServerInfoResponse):
    if data.coop_url is None:
        raise SchemaValidationError("ServerInfoResponse.coop_url")
    if len(data.coop_url) < 1:
        raise SchemaValidationError("ServerInfoResponse.coop_url")
    if data.total_sessions is None:
        raise SchemaValidationError("ServerInfoResponse.total_sessions")
    if data.total_sessions < 0:
        raise SchemaValidationError("ServerInfoResponse.total_sessions")
    if data.total_users is None:
        raise SchemaValidationError("ServerInfoResponse.total_users")
    if data.total_users < 0:
        raise SchemaValidationError("ServerInfoResponse.total_users")
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
        if field_data is None:
            raise SchemaValidationError("Session.players")
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
        if field_data is None:
            raise SchemaValidationError("SessionPlayers.usernames")
        if len(field_data) < 1:
            raise SchemaValidationError("SessionPlayers.usernames")
    return


def validate_session_response(data: SessionResponse):
    if data.session is not None:
        pass
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


class get_server_info:
    path = "api/v0/server-info"
    method = HttpMethod.GET
    operation = "get_server_info"

    @classmethod
    def wrap(cls, handler: Callable[[HttpRequest], ServerInfoResponse | tuple[int, ServerInfoResponse]]):
        return path(cls.path, lambda *args, **kwargs: cls.handle_request(handler, *args, **kwargs), name=cls.operation)

    @json_response
    @staticmethod
    def handle_request(
        handler: Callable[[HttpRequest], ServerInfoResponse | tuple[int, ServerInfoResponse]], request: HttpRequest
    ) -> ServerInfoResponse | tuple[int, ServerInfoResponse]:
        response = handler(request)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class get_tags:
    path = "api/v0/tags"
    method = HttpMethod.GET
    operation = "get_tags"

    @classmethod
    def wrap(cls, handler: Callable[[HttpRequest], TagsResponse | tuple[int, TagsResponse]]):
        return path(cls.path, lambda *args, **kwargs: cls.handle_request(handler, *args, **kwargs), name=cls.operation)

    @json_response
    @staticmethod
    def handle_request(
        handler: Callable[[HttpRequest], TagsResponse | tuple[int, TagsResponse]], request: HttpRequest
    ) -> TagsResponse | tuple[int, TagsResponse]:
        response = handler(request)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class get_sessions:
    path = "api/v0/sessions"
    method = HttpMethod.GET
    operation = "get_sessions"

    @classmethod
    def wrap(cls, handler: Callable[[HttpRequest], SessionsResponse | tuple[int, SessionsResponse]]):
        return path(cls.path, lambda *args, **kwargs: cls.handle_request(handler, *args, **kwargs), name=cls.operation)

    @json_response
    @staticmethod
    def handle_request(
        handler: Callable[[HttpRequest], SessionsResponse | tuple[int, SessionsResponse]], request: HttpRequest
    ) -> SessionsResponse | tuple[int, SessionsResponse]:
        response = handler(request)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class get_session:
    path = "api/v0/sessions/<str:sessionid>"
    method = HttpMethod.GET
    operation = "get_session"

    @classmethod
    def wrap(cls, handler: Callable[[HttpRequest, str], SessionResponse | tuple[int, SessionResponse]]):
        return path(cls.path, lambda *args, **kwargs: cls.handle_request(handler, *args, **kwargs), name=cls.operation)

    @json_response
    @staticmethod
    def handle_request(
        handler: Callable[[HttpRequest, str], SessionResponse | tuple[int, SessionResponse]],
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> SessionResponse | tuple[int, SessionResponse]:
        response = handler(request, *args, **kwargs)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class create_session:
    path = "api/v0/sessions/create"
    method = HttpMethod.POST
    operation = "create_session"

    @classmethod
    def wrap(
        cls, handler: Callable[[HttpRequest, CreateSessionRequest], SuccessResponse | tuple[int, SuccessResponse]]
    ):
        return path(cls.path, lambda *args, **kwargs: cls.handle_request(handler, *args, **kwargs), name=cls.operation)

    @json_response
    @staticmethod
    def handle_request(
        handler: Callable[[HttpRequest, CreateSessionRequest], SuccessResponse | tuple[int, SuccessResponse]],
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> SuccessResponse | tuple[int, SuccessResponse]:
        body: CreateSessionRequest = CreateSessionRequest.schema().loads(request.body.decode())
        body.validate()
        response = handler(request, *args, **kwargs, body=body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class delete_session:
    path = "api/v0/sessions/delete"
    method = HttpMethod.POST
    operation = "delete_session"

    @classmethod
    def wrap(
        cls, handler: Callable[[HttpRequest, DeleteSessionRequest], SuccessResponse | tuple[int, SuccessResponse]]
    ):
        return path(cls.path, lambda *args, **kwargs: cls.handle_request(handler, *args, **kwargs), name=cls.operation)

    @json_response
    @staticmethod
    def handle_request(
        handler: Callable[[HttpRequest, DeleteSessionRequest], SuccessResponse | tuple[int, SuccessResponse]],
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> SuccessResponse | tuple[int, SuccessResponse]:
        body: DeleteSessionRequest = DeleteSessionRequest.schema().loads(request.body.decode())
        body.validate()
        response = handler(request, *args, **kwargs, body=body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class check_session_access:
    path = "api/v0/sessions/check-access"
    method = HttpMethod.POST
    operation = "check_session_access"

    @classmethod
    def wrap(
        cls, handler: Callable[[HttpRequest, SessionAccessRequest], SuccessResponse | tuple[int, SuccessResponse]]
    ):
        return path(cls.path, lambda *args, **kwargs: cls.handle_request(handler, *args, **kwargs), name=cls.operation)

    @json_response
    @staticmethod
    def handle_request(
        handler: Callable[[HttpRequest, SessionAccessRequest], SuccessResponse | tuple[int, SuccessResponse]],
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> SuccessResponse | tuple[int, SuccessResponse]:
        body: SessionAccessRequest = SessionAccessRequest.schema().loads(request.body.decode())
        body.validate()
        response = handler(request, *args, **kwargs, body=body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class update_sessions_players:
    path = "api/v0/sessions/session-players"
    method = HttpMethod.POST
    operation = "update_sessions_players"

    @classmethod
    def wrap(cls, handler: Callable[[HttpRequest, SessionsPlayersRequest], Empty | tuple[int, Empty]]):
        return path(cls.path, lambda *args, **kwargs: cls.handle_request(handler, *args, **kwargs), name=cls.operation)

    @json_response
    @staticmethod
    def handle_request(
        handler: Callable[[HttpRequest, SessionsPlayersRequest], Empty | tuple[int, Empty]],
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> Empty | tuple[int, Empty]:
        body: SessionsPlayersRequest = SessionsPlayersRequest.schema().loads(request.body.decode())
        body.validate()
        response = handler(request, *args, **kwargs, body=body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class get_announcements:
    path = "api/v0/announcements"
    method = HttpMethod.GET
    operation = "get_announcements"

    @classmethod
    def wrap(cls, handler: Callable[[HttpRequest], AnnouncementsResponse | tuple[int, AnnouncementsResponse]]):
        return path(cls.path, lambda *args, **kwargs: cls.handle_request(handler, *args, **kwargs), name=cls.operation)

    @json_response
    @staticmethod
    def handle_request(
        handler: Callable[[HttpRequest], AnnouncementsResponse | tuple[int, AnnouncementsResponse]],
        request: HttpRequest,
    ) -> AnnouncementsResponse | tuple[int, AnnouncementsResponse]:
        response = handler(request)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class get_profile:
    path = "api/v0/auth/profile"
    method = HttpMethod.GET
    operation = "get_profile"

    @classmethod
    def wrap(cls, handler: Callable[[HttpRequest], ProfileInfoResponse | tuple[int, ProfileInfoResponse]]):
        return path(cls.path, lambda *args, **kwargs: cls.handle_request(handler, *args, **kwargs), name=cls.operation)

    @json_response
    @staticmethod
    def handle_request(
        handler: Callable[[HttpRequest], ProfileInfoResponse | tuple[int, ProfileInfoResponse]], request: HttpRequest
    ) -> ProfileInfoResponse | tuple[int, ProfileInfoResponse]:
        response = handler(request)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class change_username:
    path = "api/v0/auth/change-username"
    method = HttpMethod.POST
    operation = "change_username"

    @classmethod
    def wrap(
        cls, handler: Callable[[HttpRequest, ChangeUsernameRequest], SuccessResponse | tuple[int, SuccessResponse]]
    ):
        return path(cls.path, lambda *args, **kwargs: cls.handle_request(handler, *args, **kwargs), name=cls.operation)

    @json_response
    @staticmethod
    def handle_request(
        handler: Callable[[HttpRequest, ChangeUsernameRequest], SuccessResponse | tuple[int, SuccessResponse]],
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> SuccessResponse | tuple[int, SuccessResponse]:
        body: ChangeUsernameRequest = ChangeUsernameRequest.schema().loads(request.body.decode())
        body.validate()
        response = handler(request, *args, **kwargs, body=body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class regenerate_token:
    path = "api/v0/auth/regenerate-token"
    method = HttpMethod.GET
    operation = "regenerate_token"

    @classmethod
    def wrap(cls, handler: Callable[[HttpRequest], Empty | tuple[int, Empty]]):
        return path(cls.path, lambda *args, **kwargs: cls.handle_request(handler, *args, **kwargs), name=cls.operation)

    @json_response
    @staticmethod
    def handle_request(
        handler: Callable[[HttpRequest], Empty | tuple[int, Empty]], request: HttpRequest
    ) -> Empty | tuple[int, Empty]:
        response = handler(request)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class login:
    path = "api/v0/auth/login"
    method = HttpMethod.POST
    operation = "login"

    @classmethod
    def wrap(cls, handler: Callable[[HttpRequest, LoginRequest], SuccessResponse | tuple[int, SuccessResponse]]):
        return path(cls.path, lambda *args, **kwargs: cls.handle_request(handler, *args, **kwargs), name=cls.operation)

    @json_response
    @staticmethod
    def handle_request(
        handler: Callable[[HttpRequest, LoginRequest], SuccessResponse | tuple[int, SuccessResponse]],
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> SuccessResponse | tuple[int, SuccessResponse]:
        body: LoginRequest = LoginRequest.schema().loads(request.body.decode())
        body.validate()
        response = handler(request, *args, **kwargs, body=body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class register:
    path = "api/v0/auth/register"
    method = HttpMethod.POST
    operation = "register"

    @classmethod
    def wrap(cls, handler: Callable[[HttpRequest, RegisterRequest], SuccessResponse | tuple[int, SuccessResponse]]):
        return path(cls.path, lambda *args, **kwargs: cls.handle_request(handler, *args, **kwargs), name=cls.operation)

    @json_response
    @staticmethod
    def handle_request(
        handler: Callable[[HttpRequest, RegisterRequest], SuccessResponse | tuple[int, SuccessResponse]],
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> SuccessResponse | tuple[int, SuccessResponse]:
        body: RegisterRequest = RegisterRequest.schema().loads(request.body.decode())
        body.validate()
        response = handler(request, *args, **kwargs, body=body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class change_password:
    path = "api/v0/auth/change-password"
    method = HttpMethod.POST
    operation = "change_password"

    @classmethod
    def wrap(
        cls, handler: Callable[[HttpRequest, ChangePasswordRequest], SuccessResponse | tuple[int, SuccessResponse]]
    ):
        return path(cls.path, lambda *args, **kwargs: cls.handle_request(handler, *args, **kwargs), name=cls.operation)

    @json_response
    @staticmethod
    def handle_request(
        handler: Callable[[HttpRequest, ChangePasswordRequest], SuccessResponse | tuple[int, SuccessResponse]],
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> SuccessResponse | tuple[int, SuccessResponse]:
        body: ChangePasswordRequest = ChangePasswordRequest.schema().loads(request.body.decode())
        body.validate()
        response = handler(request, *args, **kwargs, body=body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class change_email:
    path = "api/v0/auth/change-email"
    method = HttpMethod.POST
    operation = "change_email"

    @classmethod
    def wrap(cls, handler: Callable[[HttpRequest, ChangeEmailRequest], SuccessResponse | tuple[int, SuccessResponse]]):
        return path(cls.path, lambda *args, **kwargs: cls.handle_request(handler, *args, **kwargs), name=cls.operation)

    @json_response
    @staticmethod
    def handle_request(
        handler: Callable[[HttpRequest, ChangeEmailRequest], SuccessResponse | tuple[int, SuccessResponse]],
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> SuccessResponse | tuple[int, SuccessResponse]:
        body: ChangeEmailRequest = ChangeEmailRequest.schema().loads(request.body.decode())
        body.validate()
        response = handler(request, *args, **kwargs, body=body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class logout:
    path = "api/v0/auth/logout"
    method = HttpMethod.GET
    operation = "logout"

    @classmethod
    def wrap(cls, handler: Callable[[HttpRequest], Empty | tuple[int, Empty]]):
        return path(cls.path, lambda *args, **kwargs: cls.handle_request(handler, *args, **kwargs), name=cls.operation)

    @json_response
    @staticmethod
    def handle_request(
        handler: Callable[[HttpRequest], Empty | tuple[int, Empty]], request: HttpRequest
    ) -> Empty | tuple[int, Empty]:
        response = handler(request)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response
