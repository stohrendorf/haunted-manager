import logging
import re
from dataclasses import dataclass
from enum import Enum
from http import HTTPStatus
from typing import Callable, List, Optional

from dataclasses_json import DataClassJsonMixin, dataclass_json
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.urls import path

from .error import SchemaValidationError
from .json_response import Validatable, json_response
from .schemas.AnnouncementEntry import AnnouncementEntry
from .schemas.AnnouncementsResponse import AnnouncementsResponse
from .schemas.ChangeEmailRequest import ChangeEmailRequest
from .schemas.ChangePasswordRequest import ChangePasswordRequest
from .schemas.ChangeUsernameRequest import ChangeUsernameRequest
from .schemas.CreateSessionRequest import CreateSessionRequest
from .schemas.Empty import Empty
from .schemas.LoginRequest import LoginRequest
from .schemas.ProfileInfoResponse import ProfileInfoResponse
from .schemas.RegisterRequest import RegisterRequest
from .schemas.ServerInfoResponse import ServerInfoResponse
from .schemas.Session import Session
from .schemas.SessionAccessRequest import SessionAccessRequest
from .schemas.SessionPlayers import SessionPlayers
from .schemas.SessionResponse import SessionResponse
from .schemas.SessionsPlayersRequest import SessionsPlayersRequest
from .schemas.SessionsResponse import SessionsResponse
from .schemas.SessionTag import SessionTag
from .schemas.SuccessResponse import SuccessResponse
from .schemas.Tag import Tag
from .schemas.TagsResponse import TagsResponse
from .schemas.TimeSpan import TimeSpan


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"


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
