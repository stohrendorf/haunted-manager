import logging
import re
from dataclasses import dataclass
from enum import Enum
from http import HTTPStatus
from typing import Callable, List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.urls import path

from .json_response import Validatable, json_response


class SchemaValidationError(Exception):
    pass


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"


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
        return


@dataclass_json
@dataclass(kw_only=True)
class AnnouncementsResponse(DataClassJsonMixin, Validatable):
    announcements: List["AnnouncementEntry"]

    def validate(self):
        if self.announcements is None:
            raise SchemaValidationError("AnnouncementsResponse.announcements is null")
        for self_announcements_entry in self.announcements:
            self_announcements_entry.validate()
        return


@dataclass_json
@dataclass(kw_only=True)
class ChangeEmailRequest(DataClassJsonMixin, Validatable):
    email: str

    def validate(self):
        if self.email is None:
            raise SchemaValidationError("ChangeEmailRequest.email is null")
        if len(self.email) < 1:
            raise SchemaValidationError("ChangeEmailRequest.email is too short")
        return


@dataclass_json
@dataclass(kw_only=True)
class ChangePasswordRequest(DataClassJsonMixin, Validatable):
    password: str

    def validate(self):
        if self.password is None:
            raise SchemaValidationError("ChangePasswordRequest.password is null")
        if len(self.password) < 1:
            raise SchemaValidationError("ChangePasswordRequest.password is too short")
        return


@dataclass_json
@dataclass(kw_only=True)
class ChangeUsernameRequest(DataClassJsonMixin, Validatable):
    username: str

    def validate(self):
        if self.username is None:
            raise SchemaValidationError("ChangeUsernameRequest.username is null")
        if len(self.username) < 1:
            raise SchemaValidationError("ChangeUsernameRequest.username is too short")
        return


@dataclass_json
@dataclass(kw_only=True)
class CreateSessionRequest(DataClassJsonMixin, Validatable):
    description: str
    tags: List[int]
    time: Optional["TimeSpan"]

    def validate(self):
        if self.description is None:
            raise SchemaValidationError("CreateSessionRequest.description is null")
        if len(self.description) > 512:
            raise SchemaValidationError("CreateSessionRequest.description is too long")
        if self.tags is None:
            raise SchemaValidationError("CreateSessionRequest.tags is null")
        for self_tags_entry in self.tags:
            if self_tags_entry is None:
                raise SchemaValidationError("CreateSessionRequest.tags is null")
            pass
        if self.time is not None:
            self.time.validate()
        return


@dataclass_json
@dataclass(kw_only=True)
class Empty(DataClassJsonMixin, Validatable):
    def validate(self):
        return


@dataclass_json
@dataclass(kw_only=True)
class LoginRequest(DataClassJsonMixin, Validatable):
    password: str
    username: str

    def validate(self):
        if self.password is None:
            raise SchemaValidationError("LoginRequest.password is null")
        if len(self.password) < 1:
            raise SchemaValidationError("LoginRequest.password is too short")
        if self.username is None:
            raise SchemaValidationError("LoginRequest.username is null")
        if len(self.username) < 1:
            raise SchemaValidationError("LoginRequest.username is too short")
        return


@dataclass_json
@dataclass(kw_only=True)
class ProfileInfoResponse(DataClassJsonMixin, Validatable):
    auth_token: Optional[str]
    authenticated: bool
    email: Optional[str]
    is_staff: bool
    username: str
    verified: bool

    def validate(self):
        if self.auth_token is not None:
            if len(self.auth_token) < 1:
                raise SchemaValidationError("ProfileInfoResponse.auth_token is too short")
        if self.authenticated is None:
            raise SchemaValidationError("ProfileInfoResponse.authenticated is null")
        if self.email is not None:
            if len(self.email) < 1:
                raise SchemaValidationError("ProfileInfoResponse.email is too short")
        if self.is_staff is None:
            raise SchemaValidationError("ProfileInfoResponse.is_staff is null")
        if self.username is None:
            raise SchemaValidationError("ProfileInfoResponse.username is null")
        if len(self.username) < 1:
            raise SchemaValidationError("ProfileInfoResponse.username is too short")
        if self.verified is None:
            raise SchemaValidationError("ProfileInfoResponse.verified is null")
        return


@dataclass_json
@dataclass(kw_only=True)
class RegisterRequest(DataClassJsonMixin, Validatable):
    email: str
    password: str
    username: str

    def validate(self):
        if self.email is None:
            raise SchemaValidationError("RegisterRequest.email is null")
        if len(self.email) < 1:
            raise SchemaValidationError("RegisterRequest.email is too short")
        if self.password is None:
            raise SchemaValidationError("RegisterRequest.password is null")
        if len(self.password) < 1:
            raise SchemaValidationError("RegisterRequest.password is too short")
        if self.username is None:
            raise SchemaValidationError("RegisterRequest.username is null")
        if len(self.username) < 1:
            raise SchemaValidationError("RegisterRequest.username is too short")
        return


@dataclass_json
@dataclass(kw_only=True)
class ServerInfoResponse(DataClassJsonMixin, Validatable):
    coop_url: str
    total_sessions: int
    total_users: int

    def validate(self):
        if self.coop_url is None:
            raise SchemaValidationError("ServerInfoResponse.coop_url is null")
        if len(self.coop_url) < 1:
            raise SchemaValidationError("ServerInfoResponse.coop_url is too short")
        if self.total_sessions is None:
            raise SchemaValidationError("ServerInfoResponse.total_sessions is null")
        if self.total_sessions < 0:
            raise SchemaValidationError("ServerInfoResponse.total_sessions has a value below minimum")
        if self.total_users is None:
            raise SchemaValidationError("ServerInfoResponse.total_users is null")
        if self.total_users < 0:
            raise SchemaValidationError("ServerInfoResponse.total_users has a value below minimum")
        return


@dataclass_json
@dataclass(kw_only=True)
class Session(DataClassJsonMixin, Validatable):
    description: str
    id: str
    owner: str
    players: List[str]
    tags: List["SessionTag"]
    time: Optional["TimeSpan"]

    def validate(self):
        if self.description is None:
            raise SchemaValidationError("Session.description is null")
        if self.id is None:
            raise SchemaValidationError("Session.id is null")
        if len(self.id) < 1:
            raise SchemaValidationError("Session.id is too short")
        if self.owner is None:
            raise SchemaValidationError("Session.owner is null")
        if len(self.owner) < 1:
            raise SchemaValidationError("Session.owner is too short")
        if self.players is None:
            raise SchemaValidationError("Session.players is null")
        for self_players_entry in self.players:
            if self_players_entry is None:
                raise SchemaValidationError("Session.players is null")
            if len(self_players_entry) < 1:
                raise SchemaValidationError("Session.players is too short")
        if self.tags is None:
            raise SchemaValidationError("Session.tags is null")
        for self_tags_entry in self.tags:
            self_tags_entry.validate()
        if self.time is not None:
            self.time.validate()
        return


@dataclass_json
@dataclass(kw_only=True)
class SessionAccessRequest(DataClassJsonMixin, Validatable):
    api_key: str
    auth_token: str
    session_id: str
    username: str

    def validate(self):
        if self.api_key is None:
            raise SchemaValidationError("SessionAccessRequest.api_key is null")
        if len(self.api_key) < 1:
            raise SchemaValidationError("SessionAccessRequest.api_key is too short")
        if self.auth_token is None:
            raise SchemaValidationError("SessionAccessRequest.auth_token is null")
        if len(self.auth_token) < 1:
            raise SchemaValidationError("SessionAccessRequest.auth_token is too short")
        if self.session_id is None:
            raise SchemaValidationError("SessionAccessRequest.session_id is null")
        if len(self.session_id) < 1:
            raise SchemaValidationError("SessionAccessRequest.session_id is too short")
        if self.username is None:
            raise SchemaValidationError("SessionAccessRequest.username is null")
        if len(self.username) < 1:
            raise SchemaValidationError("SessionAccessRequest.username is too short")
        return


@dataclass_json
@dataclass(kw_only=True)
class SessionPlayers(DataClassJsonMixin, Validatable):
    session_id: str
    usernames: List[str]

    def validate(self):
        if self.session_id is None:
            raise SchemaValidationError("SessionPlayers.session_id is null")
        if len(self.session_id) < 1:
            raise SchemaValidationError("SessionPlayers.session_id is too short")
        if self.usernames is None:
            raise SchemaValidationError("SessionPlayers.usernames is null")
        for self_usernames_entry in self.usernames:
            if self_usernames_entry is None:
                raise SchemaValidationError("SessionPlayers.usernames is null")
            if len(self_usernames_entry) < 1:
                raise SchemaValidationError("SessionPlayers.usernames is too short")
        return


@dataclass_json
@dataclass(kw_only=True)
class SessionResponse(DataClassJsonMixin, Validatable):
    session: Optional["Session"]

    def validate(self):
        if self.session is not None:
            self.session.validate()
        return


@dataclass_json
@dataclass(kw_only=True)
class SessionTag(DataClassJsonMixin, Validatable):
    description: str
    name: str

    def validate(self):
        if self.description is None:
            raise SchemaValidationError("SessionTag.description is null")
        if len(self.description) < 1:
            raise SchemaValidationError("SessionTag.description is too short")
        if self.name is None:
            raise SchemaValidationError("SessionTag.name is null")
        if len(self.name) < 1:
            raise SchemaValidationError("SessionTag.name is too short")
        return


@dataclass_json
@dataclass(kw_only=True)
class SessionsPlayersRequest(DataClassJsonMixin, Validatable):
    api_key: str
    sessions: List["SessionPlayers"]

    def validate(self):
        if self.api_key is None:
            raise SchemaValidationError("SessionsPlayersRequest.api_key is null")
        if len(self.api_key) < 1:
            raise SchemaValidationError("SessionsPlayersRequest.api_key is too short")
        if self.sessions is None:
            raise SchemaValidationError("SessionsPlayersRequest.sessions is null")
        for self_sessions_entry in self.sessions:
            self_sessions_entry.validate()
        return


@dataclass_json
@dataclass(kw_only=True)
class SessionsResponse(DataClassJsonMixin, Validatable):
    sessions: List["Session"]

    def validate(self):
        if self.sessions is None:
            raise SchemaValidationError("SessionsResponse.sessions is null")
        for self_sessions_entry in self.sessions:
            self_sessions_entry.validate()
        return


@dataclass_json
@dataclass(kw_only=True)
class SuccessResponse(DataClassJsonMixin, Validatable):
    message: str
    success: bool

    def validate(self):
        if self.message is None:
            raise SchemaValidationError("SuccessResponse.message is null")
        if self.success is None:
            raise SchemaValidationError("SuccessResponse.success is null")
        return


@dataclass_json
@dataclass(kw_only=True)
class Tag(DataClassJsonMixin, Validatable):
    description: str
    id: int
    name: str

    def validate(self):
        if self.description is None:
            raise SchemaValidationError("Tag.description is null")
        if self.id is None:
            raise SchemaValidationError("Tag.id is null")
        if self.name is None:
            raise SchemaValidationError("Tag.name is null")
        if len(self.name) < 1:
            raise SchemaValidationError("Tag.name is too short")
        return


@dataclass_json
@dataclass(kw_only=True)
class TagsResponse(DataClassJsonMixin, Validatable):
    tags: List["Tag"]

    def validate(self):
        if self.tags is None:
            raise SchemaValidationError("TagsResponse.tags is null")
        for self_tags_entry in self.tags:
            self_tags_entry.validate()
        return


@dataclass_json
@dataclass(kw_only=True)
class TimeSpan(DataClassJsonMixin, Validatable):
    end: str
    start: str

    def validate(self):
        if self.end is None:
            raise SchemaValidationError("TimeSpan.end is null")
        if not re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]+(\+[0-9]{2}:[0-9]{2}|Z)", self.end
        ):
            raise SchemaValidationError("TimeSpan.end has an invalid format")
        if self.start is None:
            raise SchemaValidationError("TimeSpan.start is null")
        if not re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]+(\+[0-9]{2}:[0-9]{2}|Z)", self.start
        ):
            raise SchemaValidationError("TimeSpan.start has an invalid format")
        return


def validate_iso_date_time(data: Optional[str]):
    if data is None:
        raise SchemaValidationError("IsoDateTime is null")
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]+(\+[0-9]{2}:[0-9]{2}|Z)", data):
        raise SchemaValidationError("IsoDateTime has an invalid format")
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
        def dispatch(request: HttpRequest) -> JsonResponse:
            if request.method == "GET":
                return cls.do_get(request, get_handler)
            return JsonResponse(data={}, status=HTTPStatus.METHOD_NOT_ALLOWED)

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_get(
        request: HttpRequest, handler: Callable[[HttpRequest], ServerInfoResponse | tuple[int, ServerInfoResponse]]
    ) -> ServerInfoResponse | tuple[int, ServerInfoResponse] | JsonResponse:
        response = handler(request)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
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
        def dispatch(request: HttpRequest) -> JsonResponse:
            if request.method == "GET":
                return cls.do_get(request, get_handler)
            return JsonResponse(data={}, status=HTTPStatus.METHOD_NOT_ALLOWED)

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_get(
        request: HttpRequest, handler: Callable[[HttpRequest], TagsResponse | tuple[int, TagsResponse]]
    ) -> TagsResponse | tuple[int, TagsResponse] | JsonResponse:
        response = handler(request)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
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
        def dispatch(request: HttpRequest) -> JsonResponse:
            if request.method == "GET":
                return cls.do_get(request, get_handler)
            if request.method == "POST":
                return cls.do_post(request, post_handler)
            return JsonResponse(data={}, status=HTTPStatus.METHOD_NOT_ALLOWED)

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_get(
        request: HttpRequest, handler: Callable[[HttpRequest], SessionsResponse | tuple[int, SessionsResponse]]
    ) -> SessionsResponse | tuple[int, SessionsResponse] | JsonResponse:
        response = handler(request)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        return code, response

    @json_response
    @staticmethod
    def do_post(
        request: HttpRequest,
        handler: Callable[[HttpRequest, CreateSessionRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ) -> SuccessResponse | tuple[int, SuccessResponse] | JsonResponse:
        body: CreateSessionRequest = CreateSessionRequest.schema().loads(request.body.decode())
        try:
            body.validate()
        except SchemaValidationError as e:
            logging.error("request validation failed", exc_info=True)
            return JsonResponse(status=HttpResponseBadRequest.status_code, data={"message": str(e)})
        response = handler(request, body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        return code, response


class session:
    path = "api/v0/sessions/<str:session_id>"
    name = "session"

    @classmethod
    def wrap(
        cls,
        *,
        get_handler: Callable[[HttpRequest, str], SessionResponse | tuple[int, SessionResponse]],
        post_handler: Callable[[HttpRequest, str, CreateSessionRequest], SuccessResponse | tuple[int, SuccessResponse]],
        delete_handler: Callable[[HttpRequest, str], SuccessResponse | tuple[int, SuccessResponse]],
    ):
        def dispatch(request: HttpRequest, session_id: str) -> JsonResponse:
            if request.method == "GET":
                return cls.do_get(request, get_handler, session_id)
            if request.method == "POST":
                return cls.do_post(request, post_handler, session_id)
            if request.method == "DELETE":
                return cls.do_delete(request, delete_handler, session_id)
            return JsonResponse(data={}, status=HTTPStatus.METHOD_NOT_ALLOWED)

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_get(
        request: HttpRequest,
        handler: Callable[[HttpRequest, str], SessionResponse | tuple[int, SessionResponse]],
        session_id: str,
    ) -> SessionResponse | tuple[int, SessionResponse] | JsonResponse:
        response = handler(request, session_id)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        return code, response

    @json_response
    @staticmethod
    def do_post(
        request: HttpRequest,
        handler: Callable[[HttpRequest, str, CreateSessionRequest], SuccessResponse | tuple[int, SuccessResponse]],
        session_id: str,
    ) -> SuccessResponse | tuple[int, SuccessResponse] | JsonResponse:
        body: CreateSessionRequest = CreateSessionRequest.schema().loads(request.body.decode())
        try:
            body.validate()
        except SchemaValidationError as e:
            logging.error("request validation failed", exc_info=True)
            return JsonResponse(status=HttpResponseBadRequest.status_code, data={"message": str(e)})
        response = handler(request, session_id, body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        return code, response

    @json_response
    @staticmethod
    def do_delete(
        request: HttpRequest,
        handler: Callable[[HttpRequest, str], SuccessResponse | tuple[int, SuccessResponse]],
        session_id: str,
    ) -> SuccessResponse | tuple[int, SuccessResponse] | JsonResponse:
        response = handler(request, session_id)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
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
        def dispatch(request: HttpRequest) -> JsonResponse:
            if request.method == "POST":
                return cls.do_post(request, post_handler)
            return JsonResponse(data={}, status=HTTPStatus.METHOD_NOT_ALLOWED)

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_post(
        request: HttpRequest,
        handler: Callable[[HttpRequest, SessionAccessRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ) -> SuccessResponse | tuple[int, SuccessResponse] | JsonResponse:
        body: SessionAccessRequest = SessionAccessRequest.schema().loads(request.body.decode())
        try:
            body.validate()
        except SchemaValidationError as e:
            logging.error("request validation failed", exc_info=True)
            return JsonResponse(status=HttpResponseBadRequest.status_code, data={"message": str(e)})
        response = handler(request, body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
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
        def dispatch(request: HttpRequest) -> JsonResponse:
            if request.method == "POST":
                return cls.do_post(request, post_handler)
            return JsonResponse(data={}, status=HTTPStatus.METHOD_NOT_ALLOWED)

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_post(
        request: HttpRequest, handler: Callable[[HttpRequest, SessionsPlayersRequest], Empty | tuple[int, Empty]]
    ) -> Empty | tuple[int, Empty] | JsonResponse:
        body: SessionsPlayersRequest = SessionsPlayersRequest.schema().loads(request.body.decode())
        try:
            body.validate()
        except SchemaValidationError as e:
            logging.error("request validation failed", exc_info=True)
            return JsonResponse(status=HttpResponseBadRequest.status_code, data={"message": str(e)})
        response = handler(request, body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
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
        def dispatch(request: HttpRequest) -> JsonResponse:
            if request.method == "GET":
                return cls.do_get(request, get_handler)
            return JsonResponse(data={}, status=HTTPStatus.METHOD_NOT_ALLOWED)

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_get(
        request: HttpRequest,
        handler: Callable[[HttpRequest], AnnouncementsResponse | tuple[int, AnnouncementsResponse]],
    ) -> AnnouncementsResponse | tuple[int, AnnouncementsResponse] | JsonResponse:
        response = handler(request)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
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
        def dispatch(request: HttpRequest) -> JsonResponse:
            if request.method == "GET":
                return cls.do_get(request, get_handler)
            return JsonResponse(data={}, status=HTTPStatus.METHOD_NOT_ALLOWED)

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_get(
        request: HttpRequest, handler: Callable[[HttpRequest], ProfileInfoResponse | tuple[int, ProfileInfoResponse]]
    ) -> ProfileInfoResponse | tuple[int, ProfileInfoResponse] | JsonResponse:
        response = handler(request)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
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
        def dispatch(request: HttpRequest) -> JsonResponse:
            if request.method == "POST":
                return cls.do_post(request, post_handler)
            return JsonResponse(data={}, status=HTTPStatus.METHOD_NOT_ALLOWED)

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_post(
        request: HttpRequest,
        handler: Callable[[HttpRequest, ChangeUsernameRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ) -> SuccessResponse | tuple[int, SuccessResponse] | JsonResponse:
        body: ChangeUsernameRequest = ChangeUsernameRequest.schema().loads(request.body.decode())
        try:
            body.validate()
        except SchemaValidationError as e:
            logging.error("request validation failed", exc_info=True)
            return JsonResponse(status=HttpResponseBadRequest.status_code, data={"message": str(e)})
        response = handler(request, body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
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
        def dispatch(request: HttpRequest) -> JsonResponse:
            if request.method == "GET":
                return cls.do_get(request, get_handler)
            return JsonResponse(data={}, status=HTTPStatus.METHOD_NOT_ALLOWED)

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_get(
        request: HttpRequest, handler: Callable[[HttpRequest], Empty | tuple[int, Empty]]
    ) -> Empty | tuple[int, Empty] | JsonResponse:
        response = handler(request)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
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
        def dispatch(request: HttpRequest) -> JsonResponse:
            if request.method == "POST":
                return cls.do_post(request, post_handler)
            return JsonResponse(data={}, status=HTTPStatus.METHOD_NOT_ALLOWED)

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_post(
        request: HttpRequest,
        handler: Callable[[HttpRequest, LoginRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ) -> SuccessResponse | tuple[int, SuccessResponse] | JsonResponse:
        body: LoginRequest = LoginRequest.schema().loads(request.body.decode())
        try:
            body.validate()
        except SchemaValidationError as e:
            logging.error("request validation failed", exc_info=True)
            return JsonResponse(status=HttpResponseBadRequest.status_code, data={"message": str(e)})
        response = handler(request, body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
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
        def dispatch(request: HttpRequest) -> JsonResponse:
            if request.method == "POST":
                return cls.do_post(request, post_handler)
            return JsonResponse(data={}, status=HTTPStatus.METHOD_NOT_ALLOWED)

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_post(
        request: HttpRequest,
        handler: Callable[[HttpRequest, RegisterRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ) -> SuccessResponse | tuple[int, SuccessResponse] | JsonResponse:
        body: RegisterRequest = RegisterRequest.schema().loads(request.body.decode())
        try:
            body.validate()
        except SchemaValidationError as e:
            logging.error("request validation failed", exc_info=True)
            return JsonResponse(status=HttpResponseBadRequest.status_code, data={"message": str(e)})
        response = handler(request, body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
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
        def dispatch(request: HttpRequest) -> JsonResponse:
            if request.method == "POST":
                return cls.do_post(request, post_handler)
            return JsonResponse(data={}, status=HTTPStatus.METHOD_NOT_ALLOWED)

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_post(
        request: HttpRequest,
        handler: Callable[[HttpRequest, ChangePasswordRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ) -> SuccessResponse | tuple[int, SuccessResponse] | JsonResponse:
        body: ChangePasswordRequest = ChangePasswordRequest.schema().loads(request.body.decode())
        try:
            body.validate()
        except SchemaValidationError as e:
            logging.error("request validation failed", exc_info=True)
            return JsonResponse(status=HttpResponseBadRequest.status_code, data={"message": str(e)})
        response = handler(request, body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
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
        def dispatch(request: HttpRequest) -> JsonResponse:
            if request.method == "POST":
                return cls.do_post(request, post_handler)
            return JsonResponse(data={}, status=HTTPStatus.METHOD_NOT_ALLOWED)

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_post(
        request: HttpRequest,
        handler: Callable[[HttpRequest, ChangeEmailRequest], SuccessResponse | tuple[int, SuccessResponse]],
    ) -> SuccessResponse | tuple[int, SuccessResponse] | JsonResponse:
        body: ChangeEmailRequest = ChangeEmailRequest.schema().loads(request.body.decode())
        try:
            body.validate()
        except SchemaValidationError as e:
            logging.error("request validation failed", exc_info=True)
            return JsonResponse(status=HttpResponseBadRequest.status_code, data={"message": str(e)})
        response = handler(request, body)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
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
        def dispatch(request: HttpRequest) -> JsonResponse:
            if request.method == "GET":
                return cls.do_get(request, get_handler)
            return JsonResponse(data={}, status=HTTPStatus.METHOD_NOT_ALLOWED)

        return path(cls.path, dispatch, name=cls.name)

    @json_response
    @staticmethod
    def do_get(
        request: HttpRequest, handler: Callable[[HttpRequest], Empty | tuple[int, Empty]]
    ) -> Empty | tuple[int, Empty] | JsonResponse:
        response = handler(request)
        if isinstance(response, tuple):
            code, response = response
        else:
            code = HttpResponse.status_code
        return code, response
