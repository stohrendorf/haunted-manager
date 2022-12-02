import logging
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.transaction import atomic
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt

from haunted_auth.models import ApiKey
from hsutils.auth import require_authenticated
from hsutils.rest_helper import parse_datetime
from hsutils.viewmodels import (
    CreateSessionRequest,
    Empty,
    Session,
    SessionAccessRequest,
    SessionResponse,
    SessionsPlayersRequest,
    SessionsResponse,
    SessionTag,
    SuccessResponse,
    Tag,
    TagsResponse,
    TimeSpan,
)

from .models import Session as SessionModel
from .models import Tag as TagModel

User = get_user_model()


def get_tags(request: HttpRequest) -> TagsResponse:
    return TagsResponse(
        tags=[
            Tag(
                id=tag.id,
                name=tag.name,
                description=tag.description,
            )
            for tag in TagModel.objects.order_by("name").all()
        ],
    )


def session_to_response(session: SessionModel) -> Session:
    return Session(
        id=session.key.hex,
        tags=[
            SessionTag(
                name=t.name,
                description=t.description,
            )
            for t in session.tags.all()
        ],
        owner=session.owner.username,
        description=session.description,
        players=[u.username for u in session.players.all()],
        time=TimeSpan(
            start=session.start.isoformat(),
            end=session.end.isoformat(),
        )
        if session.is_event
        else None,
        private=session.private,
    )


def get_sessions(request: HttpRequest) -> SessionsResponse:
    if request.user.is_staff or request.user.is_superuser:
        sessions = SessionModel.objects
    else:
        sessions = SessionModel.objects.filter(Q(private=False) | Q(private=True, owner_id=request.user.id))
    return SessionsResponse(
        sessions=[session_to_response(session) for session in sessions.order_by("-created_at").all()],
    )


def get_session(request: HttpRequest, session_id: str) -> SessionResponse | tuple[int, SessionResponse]:
    try:
        session = SessionModel.objects.get(key=session_id)
    except SessionModel.DoesNotExist:
        return HTTPStatus.NOT_FOUND, SessionResponse(session=None)

    if request.user.is_staff or request.user.is_superuser:
        pass
    elif session.private and session.owner != request.user:
        return HTTPStatus.NOT_FOUND, SessionResponse(session=None)

    return SessionResponse(session=session_to_response(session))


def _apply_session_properties(
    request: HttpRequest,
    session: SessionModel,
    body: CreateSessionRequest,
) -> SuccessResponse | tuple[int, SuccessResponse]:
    if request.user.is_staff or request.user.is_superuser:
        pass
    elif request.user != session.owner:
        return HTTPStatus.FORBIDDEN, SuccessResponse(
            message="not allowed to edit this session",
            success=False,
        )

    session.tags.set(body.tags)
    session.description = body.description

    if body.time is not None:
        session.start = parse_datetime(body.time.start)
        session.end = parse_datetime(body.time.end)
    else:
        session.start = None
        session.end = None

    session.private = body.private
    session.save()
    return SuccessResponse(message="", success=True)


@require_authenticated(response=SuccessResponse(success=False, message="not allowed"))
def edit_session(
    request: HttpRequest,
    session_id: str,
    body: CreateSessionRequest,
) -> SuccessResponse | tuple[int, SuccessResponse]:
    try:
        session = SessionModel.objects.get(key=session_id)
    except SessionModel.DoesNotExist:
        return HTTPStatus.NOT_FOUND, SuccessResponse(message="invalid session id", success=False)

    return _apply_session_properties(request, session, body)


@require_authenticated(response=SuccessResponse(success=False, message="not allowed"))
def delete_session(request: HttpRequest, session_id: str) -> tuple[int, SuccessResponse] | SuccessResponse:
    try:
        session = SessionModel.objects.get(key=session_id)
    except SessionModel.DoesNotExist:
        return HTTPStatus.NOT_FOUND, SuccessResponse(
            message=f"session {session_id} not found",
            success=False,
        )

    if request.user.is_staff or request.user.is_superuser:
        pass
    elif session.owner != request.user:
        return HTTPStatus.FORBIDDEN, SuccessResponse(
            message=f"not allowed to delete session {session_id}",
            success=False,
        )
    session.delete()
    return SuccessResponse(
        message=f"session {session_id} deleted",
        success=True,
    )


@csrf_exempt
def check_session_access(
    request: HttpRequest,
    body: SessionAccessRequest,
) -> SuccessResponse | tuple[int, SuccessResponse]:
    if body.api_key != settings.COOP_API_KEY:
        return HTTPStatus.UNAUTHORIZED, SuccessResponse(success=False, message="invalid api key")

    try:
        user = User.objects.get(username=body.username)
    except User.DoesNotExist:
        return HTTPStatus.NOT_FOUND, SuccessResponse(success=False, message="user does not exist")
    except Exception:
        logging.error("unexpected error while retrieving user", exc_info=True)
        return HTTPStatus.INTERNAL_SERVER_ERROR, SuccessResponse(
            success=False,
            message="unexpected error while retrieving user",
        )

    if not user.is_active:
        return HTTPStatus.NOT_FOUND, SuccessResponse(success=False, message="user is inactive")

    try:
        auth_token = ApiKey.objects.get(owner=user)
    except ApiKey.DoesNotExist:
        return HTTPStatus.NOT_FOUND, SuccessResponse(success=False, message="auth token not found")
    except Exception:
        logging.error("unexpected error while checking auth token", exc_info=True)
        return HTTPStatus.INTERNAL_SERVER_ERROR, SuccessResponse(
            success=False,
            message="unexpected error while checking auth token",
        )

    if auth_token.key.hex != body.auth_token:
        return HTTPStatus.UNAUTHORIZED, SuccessResponse(success=False, message="invalid auth token")
    if not SessionModel.objects.filter(key=body.session_id).exists():
        return HTTPStatus.NOT_FOUND, SuccessResponse(success=False, message="session does not exist")
    return SuccessResponse(success=True, message="")


@csrf_exempt
@atomic
def update_sessions_players(request: HttpRequest, body: SessionsPlayersRequest) -> Empty | tuple[int, Empty]:
    if body.api_key != settings.COOP_API_KEY:
        return HTTPStatus.UNAUTHORIZED, Empty()

    for db_session in SessionModel.objects.all():
        db_session.players.clear()
    for session in body.sessions:
        try:
            db_session = SessionModel.objects.get(key=session.session_id)
        except SessionModel.DoesNotExist:
            continue
        for user in session.usernames:
            try:
                db_user = User.objects.get(username=user)
            except User.DoesNotExist:
                continue
            db_session.players.add(db_user)
    return Empty()


@atomic
@require_authenticated(response=SuccessResponse(success=False, message="not allowed"))
def create_session(
    request: HttpRequest,
    body: CreateSessionRequest,
) -> tuple[int, SuccessResponse] | SuccessResponse:
    session = SessionModel.objects.create(
        owner=request.user,
        description=body.description,
        private=body.private,
    )

    return HTTPStatus.CREATED, _apply_session_properties(request, session, body)
