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
        raise SchemaValidationError("AnnouncementEntry.background_color is null")
    if len(data.background_color) < 1:
        raise SchemaValidationError("AnnouncementEntry.background_color is too short")
    if data.message is None:
        raise SchemaValidationError("AnnouncementEntry.message is null")
    if len(data.message) < 1:
        raise SchemaValidationError("AnnouncementEntry.message is too short")
    if data.text_color is None:
        raise SchemaValidationError("AnnouncementEntry.text_color is null")
    if len(data.text_color) < 1:
        raise SchemaValidationError("AnnouncementEntry.text_color is too short")
    return


def validate_announcements_response(data: AnnouncementsResponse):
    if data.announcements is None:
        raise SchemaValidationError("AnnouncementsResponse.announcements is null")
    for data_announcements_entry in data.announcements:
        validate_announcement_entry(data_announcements_entry)
    return


def validate_change_email_request(data: ChangeEmailRequest):
    if data.email is None:
        raise SchemaValidationError("ChangeEmailRequest.email is null")
    if len(data.email) < 1:
        raise SchemaValidationError("ChangeEmailRequest.email is too short")
    return


def validate_change_password_request(data: ChangePasswordRequest):
    if data.password is None:
        raise SchemaValidationError("ChangePasswordRequest.password is null")
    if len(data.password) < 1:
        raise SchemaValidationError("ChangePasswordRequest.password is too short")
    return


def validate_change_username_request(data: ChangeUsernameRequest):
    if data.username is None:
        raise SchemaValidationError("ChangeUsernameRequest.username is null")
    if len(data.username) < 1:
        raise SchemaValidationError("ChangeUsernameRequest.username is too short")
    return


def validate_create_session_request(data: CreateSessionRequest):
    if data.description is None:
        raise SchemaValidationError("CreateSessionRequest.description is null")
    if data.tags is None:
        raise SchemaValidationError("CreateSessionRequest.tags is null")
    for data_tags_entry in data.tags:
        if data_tags_entry is None:
            raise SchemaValidationError("CreateSessionRequest.tags is null")
        pass
    return


def validate_empty(data: Empty):
    return


def validate_login_request(data: LoginRequest):
    if data.password is None:
        raise SchemaValidationError("LoginRequest.password is null")
    if len(data.password) < 1:
        raise SchemaValidationError("LoginRequest.password is too short")
    if data.username is None:
        raise SchemaValidationError("LoginRequest.username is null")
    if len(data.username) < 1:
        raise SchemaValidationError("LoginRequest.username is too short")
    return


def validate_profile_info_response(data: ProfileInfoResponse):
    if data.auth_token is not None:
        if len(data.auth_token) < 1:
            raise SchemaValidationError("ProfileInfoResponse.auth_token is too short")
    if data.authenticated is None:
        raise SchemaValidationError("ProfileInfoResponse.authenticated is null")
    if data.email is not None:
        if len(data.email) < 1:
            raise SchemaValidationError("ProfileInfoResponse.email is too short")
    if data.username is None:
        raise SchemaValidationError("ProfileInfoResponse.username is null")
    if len(data.username) < 1:
        raise SchemaValidationError("ProfileInfoResponse.username is too short")
    if data.verified is None:
        raise SchemaValidationError("ProfileInfoResponse.verified is null")
    return


def validate_register_request(data: RegisterRequest):
    if data.email is None:
        raise SchemaValidationError("RegisterRequest.email is null")
    if len(data.email) < 1:
        raise SchemaValidationError("RegisterRequest.email is too short")
    if data.password is None:
        raise SchemaValidationError("RegisterRequest.password is null")
    if len(data.password) < 1:
        raise SchemaValidationError("RegisterRequest.password is too short")
    if data.username is None:
        raise SchemaValidationError("RegisterRequest.username is null")
    if len(data.username) < 1:
        raise SchemaValidationError("RegisterRequest.username is too short")
    return


def validate_server_info_response(data: ServerInfoResponse):
    if data.coop_url is None:
        raise SchemaValidationError("ServerInfoResponse.coop_url is null")
    if len(data.coop_url) < 1:
        raise SchemaValidationError("ServerInfoResponse.coop_url is too short")
    if data.total_sessions is None:
        raise SchemaValidationError("ServerInfoResponse.total_sessions is null")
    if data.total_sessions < 0:
        raise SchemaValidationError("ServerInfoResponse.total_sessions has a value below minimum")
    if data.total_users is None:
        raise SchemaValidationError("ServerInfoResponse.total_users is null")
    if data.total_users < 0:
        raise SchemaValidationError("ServerInfoResponse.total_users has a value below minimum")
    return


def validate_session(data: Session):
    if data.description is None:
        raise SchemaValidationError("Session.description is null")
    if data.id is None:
        raise SchemaValidationError("Session.id is null")
    if len(data.id) < 1:
        raise SchemaValidationError("Session.id is too short")
    if data.owner is None:
        raise SchemaValidationError("Session.owner is null")
    if len(data.owner) < 1:
        raise SchemaValidationError("Session.owner is too short")
    if data.players is None:
        raise SchemaValidationError("Session.players is null")
    for data_players_entry in data.players:
        if data_players_entry is None:
            raise SchemaValidationError("Session.players is null")
        if len(data_players_entry) < 1:
            raise SchemaValidationError("Session.players is too short")
    if data.tags is None:
        raise SchemaValidationError("Session.tags is null")
    for data_tags_entry in data.tags:
        validate_session_tag(data_tags_entry)
    return


def validate_session_access_request(data: SessionAccessRequest):
    if data.api_key is None:
        raise SchemaValidationError("SessionAccessRequest.api_key is null")
    if len(data.api_key) < 1:
        raise SchemaValidationError("SessionAccessRequest.api_key is too short")
    if data.auth_token is None:
        raise SchemaValidationError("SessionAccessRequest.auth_token is null")
    if len(data.auth_token) < 1:
        raise SchemaValidationError("SessionAccessRequest.auth_token is too short")
    if data.session_id is None:
        raise SchemaValidationError("SessionAccessRequest.session_id is null")
    if len(data.session_id) < 1:
        raise SchemaValidationError("SessionAccessRequest.session_id is too short")
    if data.username is None:
        raise SchemaValidationError("SessionAccessRequest.username is null")
    if len(data.username) < 1:
        raise SchemaValidationError("SessionAccessRequest.username is too short")
    return


def validate_session_players(data: SessionPlayers):
    if data.session_id is None:
        raise SchemaValidationError("SessionPlayers.session_id is null")
    if len(data.session_id) < 1:
        raise SchemaValidationError("SessionPlayers.session_id is too short")
    if data.usernames is None:
        raise SchemaValidationError("SessionPlayers.usernames is null")
    for data_usernames_entry in data.usernames:
        if data_usernames_entry is None:
            raise SchemaValidationError("SessionPlayers.usernames is null")
        if len(data_usernames_entry) < 1:
            raise SchemaValidationError("SessionPlayers.usernames is too short")
    return


def validate_session_response(data: SessionResponse):
    if data.session is not None:
        pass
    return


def validate_session_tag(data: SessionTag):
    if data.description is None:
        raise SchemaValidationError("SessionTag.description is null")
    if len(data.description) < 1:
        raise SchemaValidationError("SessionTag.description is too short")
    if data.name is None:
        raise SchemaValidationError("SessionTag.name is null")
    if len(data.name) < 1:
        raise SchemaValidationError("SessionTag.name is too short")
    return


def validate_sessions_players_request(data: SessionsPlayersRequest):
    if data.api_key is None:
        raise SchemaValidationError("SessionsPlayersRequest.api_key is null")
    if len(data.api_key) < 1:
        raise SchemaValidationError("SessionsPlayersRequest.api_key is too short")
    if data.sessions is None:
        raise SchemaValidationError("SessionsPlayersRequest.sessions is null")
    for data_sessions_entry in data.sessions:
        validate_session_players(data_sessions_entry)
    return


def validate_sessions_response(data: SessionsResponse):
    if data.sessions is None:
        raise SchemaValidationError("SessionsResponse.sessions is null")
    for data_sessions_entry in data.sessions:
        validate_session(data_sessions_entry)
    return


def validate_success_response(data: SuccessResponse):
    if data.message is None:
        raise SchemaValidationError("SuccessResponse.message is null")
    if data.success is None:
        raise SchemaValidationError("SuccessResponse.success is null")
    return


def validate_tag(data: Tag):
    if data.description is None:
        raise SchemaValidationError("Tag.description is null")
    if data.id is None:
        raise SchemaValidationError("Tag.id is null")
    if data.name is None:
        raise SchemaValidationError("Tag.name is null")
    if len(data.name) < 1:
        raise SchemaValidationError("Tag.name is too short")
    return


def validate_tags_response(data: TagsResponse):
    if data.tags is None:
        raise SchemaValidationError("TagsResponse.tags is null")
    for data_tags_entry in data.tags:
        validate_tag(data_tags_entry)
    return


class server_info:
    path = "api/v0/server-info"
    name = "serverInfo"

    @classmethod
    def wrap(
        cls,
        *,
        get_handler: Callable[[HttpRequest], ServerInfoResponse | tuple[int, ServerInfoResponse]],
    ):
        def dispatch(request: HttpRequest):
            if request.method == "GET":
                return cls.do_get(request, get_handler)
            raise RuntimeError

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_get(
        request: HttpRequest, handler: Callable[[HttpRequest], ServerInfoResponse | tuple[int, ServerInfoResponse]]
    ) -> ServerInfoResponse | tuple[int, ServerInfoResponse]:
        response = handler(request)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class tags:
    path = "api/v0/tags"
    name = "tags"

    @classmethod
    def wrap(
        cls,
        *,
        get_handler: Callable[[HttpRequest], TagsResponse | tuple[int, TagsResponse]],
    ):
        def dispatch(request: HttpRequest):
            if request.method == "GET":
                return cls.do_get(request, get_handler)
            raise RuntimeError

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_get(
        request: HttpRequest, handler: Callable[[HttpRequest], TagsResponse | tuple[int, TagsResponse]]
    ) -> TagsResponse | tuple[int, TagsResponse]:
        response = handler(request)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class sessions:
    path = "api/v0/sessions"
    name = "sessions"

    @classmethod
    def wrap(
        cls,
        *,
        get_handler: Callable[[HttpRequest], SessionsResponse | tuple[int, SessionsResponse]],
        post_handler: Callable[[HttpRequest, CreateSessionRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ):
        def dispatch(request: HttpRequest):
            if request.method == "GET":
                return cls.do_get(request, get_handler)
            if request.method == "POST":
                return cls.do_post(request, post_handler)
            raise RuntimeError

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_get(
        request: HttpRequest, handler: Callable[[HttpRequest], SessionsResponse | tuple[int, SessionsResponse]]
    ) -> SessionsResponse | tuple[int, SessionsResponse]:
        response = handler(request)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response

    @json_response
    @staticmethod
    def do_post(
        request: HttpRequest,
        handler: Callable[[HttpRequest, CreateSessionRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ) -> SuccessResponse | tuple[int, SuccessResponse]:
        body: CreateSessionRequest = CreateSessionRequest.schema().loads(request.body.decode())
        body.validate()
        response = handler(request, body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class session:
    path = "api/v0/sessions/<str:sessionId>"
    name = "session"

    @classmethod
    def wrap(
        cls,
        *,
        get_handler: Callable[[HttpRequest, str], SessionResponse | tuple[int, SessionResponse]],
        post_handler: Callable[[HttpRequest, str, CreateSessionRequest], SuccessResponse | tuple[int, SuccessResponse]],
        delete_handler: Callable[[HttpRequest, str], SuccessResponse | tuple[int, SuccessResponse]],
    ):
        def dispatch(request: HttpRequest, sessionId: str):
            if request.method == "GET":
                return cls.do_get(request, get_handler, sessionId)
            if request.method == "POST":
                return cls.do_post(request, post_handler, sessionId)
            if request.method == "DELETE":
                return cls.do_delete(request, delete_handler, sessionId)
            raise RuntimeError

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_get(
        request: HttpRequest,
        handler: Callable[[HttpRequest, str], SessionResponse | tuple[int, SessionResponse]],
        sessionId: str,
    ) -> SessionResponse | tuple[int, SessionResponse]:
        response = handler(request, sessionId)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response

    @json_response
    @staticmethod
    def do_post(
        request: HttpRequest,
        handler: Callable[[HttpRequest, str, CreateSessionRequest], SuccessResponse | tuple[int, SuccessResponse]],
        sessionId: str,
    ) -> SuccessResponse | tuple[int, SuccessResponse]:
        body: CreateSessionRequest = CreateSessionRequest.schema().loads(request.body.decode())
        body.validate()
        response = handler(request, sessionId, body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response

    @json_response
    @staticmethod
    def do_delete(
        request: HttpRequest,
        handler: Callable[[HttpRequest, str], SuccessResponse | tuple[int, SuccessResponse]],
        sessionId: str,
    ) -> SuccessResponse | tuple[int, SuccessResponse]:
        response = handler(request, sessionId)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class session_access:
    path = "api/v0/sessions/check-access"
    name = "sessionAccess"

    @classmethod
    def wrap(
        cls,
        *,
        post_handler: Callable[[HttpRequest, SessionAccessRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ):
        def dispatch(request: HttpRequest):
            if request.method == "POST":
                return cls.do_post(request, post_handler)
            raise RuntimeError

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_post(
        request: HttpRequest,
        handler: Callable[[HttpRequest, SessionAccessRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ) -> SuccessResponse | tuple[int, SuccessResponse]:
        body: SessionAccessRequest = SessionAccessRequest.schema().loads(request.body.decode())
        body.validate()
        response = handler(request, body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class session_players:
    path = "api/v0/sessions/session-players"
    name = "sessionPlayers"

    @classmethod
    def wrap(
        cls,
        *,
        post_handler: Callable[[HttpRequest, SessionsPlayersRequest], Empty | tuple[int, Empty]],
    ):
        def dispatch(request: HttpRequest):
            if request.method == "POST":
                return cls.do_post(request, post_handler)
            raise RuntimeError

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_post(
        request: HttpRequest, handler: Callable[[HttpRequest, SessionsPlayersRequest], Empty | tuple[int, Empty]]
    ) -> Empty | tuple[int, Empty]:
        body: SessionsPlayersRequest = SessionsPlayersRequest.schema().loads(request.body.decode())
        body.validate()
        response = handler(request, body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class announcements:
    path = "api/v0/announcements"
    name = "announcements"

    @classmethod
    def wrap(
        cls,
        *,
        get_handler: Callable[[HttpRequest], AnnouncementsResponse | tuple[int, AnnouncementsResponse]],
    ):
        def dispatch(request: HttpRequest):
            if request.method == "GET":
                return cls.do_get(request, get_handler)
            raise RuntimeError

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_get(
        request: HttpRequest,
        handler: Callable[[HttpRequest], AnnouncementsResponse | tuple[int, AnnouncementsResponse]],
    ) -> AnnouncementsResponse | tuple[int, AnnouncementsResponse]:
        response = handler(request)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class profile:
    path = "api/v0/auth/profile"
    name = "profile"

    @classmethod
    def wrap(
        cls,
        *,
        get_handler: Callable[[HttpRequest], ProfileInfoResponse | tuple[int, ProfileInfoResponse]],
    ):
        def dispatch(request: HttpRequest):
            if request.method == "GET":
                return cls.do_get(request, get_handler)
            raise RuntimeError

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_get(
        request: HttpRequest, handler: Callable[[HttpRequest], ProfileInfoResponse | tuple[int, ProfileInfoResponse]]
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
    name = "changeUsername"

    @classmethod
    def wrap(
        cls,
        *,
        post_handler: Callable[[HttpRequest, ChangeUsernameRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ):
        def dispatch(request: HttpRequest):
            if request.method == "POST":
                return cls.do_post(request, post_handler)
            raise RuntimeError

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_post(
        request: HttpRequest,
        handler: Callable[[HttpRequest, ChangeUsernameRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ) -> SuccessResponse | tuple[int, SuccessResponse]:
        body: ChangeUsernameRequest = ChangeUsernameRequest.schema().loads(request.body.decode())
        body.validate()
        response = handler(request, body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class regenerate_token:
    path = "api/v0/auth/regenerate-token"
    name = "regenerateToken"

    @classmethod
    def wrap(
        cls,
        *,
        get_handler: Callable[[HttpRequest], Empty | tuple[int, Empty]],
    ):
        def dispatch(request: HttpRequest):
            if request.method == "GET":
                return cls.do_get(request, get_handler)
            raise RuntimeError

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_get(
        request: HttpRequest, handler: Callable[[HttpRequest], Empty | tuple[int, Empty]]
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
    name = "login"

    @classmethod
    def wrap(
        cls,
        *,
        post_handler: Callable[[HttpRequest, LoginRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ):
        def dispatch(request: HttpRequest):
            if request.method == "POST":
                return cls.do_post(request, post_handler)
            raise RuntimeError

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_post(
        request: HttpRequest,
        handler: Callable[[HttpRequest, LoginRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ) -> SuccessResponse | tuple[int, SuccessResponse]:
        body: LoginRequest = LoginRequest.schema().loads(request.body.decode())
        body.validate()
        response = handler(request, body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class register:
    path = "api/v0/auth/register"
    name = "register"

    @classmethod
    def wrap(
        cls,
        *,
        post_handler: Callable[[HttpRequest, RegisterRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ):
        def dispatch(request: HttpRequest):
            if request.method == "POST":
                return cls.do_post(request, post_handler)
            raise RuntimeError

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_post(
        request: HttpRequest,
        handler: Callable[[HttpRequest, RegisterRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ) -> SuccessResponse | tuple[int, SuccessResponse]:
        body: RegisterRequest = RegisterRequest.schema().loads(request.body.decode())
        body.validate()
        response = handler(request, body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class change_password:
    path = "api/v0/auth/change-password"
    name = "changePassword"

    @classmethod
    def wrap(
        cls,
        *,
        post_handler: Callable[[HttpRequest, ChangePasswordRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ):
        def dispatch(request: HttpRequest):
            if request.method == "POST":
                return cls.do_post(request, post_handler)
            raise RuntimeError

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_post(
        request: HttpRequest,
        handler: Callable[[HttpRequest, ChangePasswordRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ) -> SuccessResponse | tuple[int, SuccessResponse]:
        body: ChangePasswordRequest = ChangePasswordRequest.schema().loads(request.body.decode())
        body.validate()
        response = handler(request, body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class change_email:
    path = "api/v0/auth/change-email"
    name = "changeEmail"

    @classmethod
    def wrap(
        cls,
        *,
        post_handler: Callable[[HttpRequest, ChangeEmailRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ):
        def dispatch(request: HttpRequest):
            if request.method == "POST":
                return cls.do_post(request, post_handler)
            raise RuntimeError

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_post(
        request: HttpRequest,
        handler: Callable[[HttpRequest, ChangeEmailRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ) -> SuccessResponse | tuple[int, SuccessResponse]:
        body: ChangeEmailRequest = ChangeEmailRequest.schema().loads(request.body.decode())
        body.validate()
        response = handler(request, body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response


class logout:
    path = "api/v0/auth/logout"
    name = "logout"

    @classmethod
    def wrap(
        cls,
        *,
        get_handler: Callable[[HttpRequest], Empty | tuple[int, Empty]],
    ):
        def dispatch(request: HttpRequest):
            if request.method == "GET":
                return cls.do_get(request, get_handler)
            raise RuntimeError

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_get(
        request: HttpRequest, handler: Callable[[HttpRequest], Empty | tuple[int, Empty]]
    ) -> Empty | tuple[int, Empty]:
        response = handler(request)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        response.validate()
        return code, response
