import logging
from typing import Union

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from django.http import HttpRequest, HttpResponseForbidden, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

from haunted_auth.models import ApiKey
from hsutils.viewmodels import (
    CreateSessionRequest,
    DeleteSessionRequest,
    Empty,
    EditSessionRequest,
    GetSessionResponse,
    Session,
    SessionAccessRequest,
    SessionsPlayersRequest,
    SessionsResponse,
    SessionTag,
    SuccessResponse,
    Tag,
    TagsResponse,
)

from .models import Session as SessionModel
from .models import Tag as TagModel

User = get_user_model()


def get_tags(request) -> TagsResponse:
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


def get_sessions(request) -> SessionsResponse:
    return SessionsResponse(
        sessions=[
            Session(
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
            )
            for session in SessionModel.objects.order_by("-created_at").all()
        ],
    )

def get_session(request: HttpRequest, id: str) -> Union[tuple[int, SuccessResponse], GetSessionResponse]:
    try:
        session = SessionModel.objects.get(key=id)
    except SessionModel.DoesNotExist:
        return HttpResponseNotFound.status_code, SuccessResponse(message=f"session {id} not found", success=False)
    return GetSessionResponse(
        session=Session(
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
        players=[]
    ))

def delete_session(request, body: DeleteSessionRequest) -> tuple[int, SuccessResponse] | SuccessResponse:
    if not request.user.is_active or not request.user.is_authenticated:
        return HttpResponseForbidden.status_code, SuccessResponse(success=False, message="not allowed")

    session = SessionModel.objects.get(key=body.session_id)
    if not session:
        return HttpResponseNotFound.status_code, SuccessResponse(
            message=f"session {body.session_id} not found",
            success=False,
        )
    if session.owner != request.user:
        return 401, SuccessResponse(
            message=f"not allowed to delete session {body.session_id}",
            success=False,
        )
    session.delete()
    return SuccessResponse(
        message=f"session {body.session_id} deleted",
        success=True,
    )

@csrf_exempt
def check_session_access(request: HttpRequest, body: SessionAccessRequest) -> SuccessResponse:
    if body.api_key != settings.COOP_API_KEY:
        return SuccessResponse(success=False, message="invalid api key")

    try:
        user = User.objects.get(username=body.username)
    except User.DoesNotExist:
        return SuccessResponse(success=False, message="user does not exist")
    except Exception:
        logging.error("unexpected error while retrieving user", exc_info=True)
        return SuccessResponse(success=False, message="unexpected error while retrieving user")

    if not user.is_active:
        return SuccessResponse(success=False, message="user is inactive")

    try:
        auth_token = ApiKey.objects.get(owner=user)
    except ApiKey.DoesNotExist:
        return SuccessResponse(success=False, message="auth token not found")
    except Exception:
        logging.error("unexpected error while checking auth token", exc_info=True)
        return SuccessResponse(success=False, message="unexpected error while checking auth token")

    if auth_token.key.hex != body.auth_token:
        return SuccessResponse(success=False, message="invalid auth token")
    if not SessionModel.objects.filter(key=body.session_id).exists():
        return SuccessResponse(success=False, message="session does not exist")
    return SuccessResponse(success=True, message="")


@csrf_exempt
@atomic
def update_sessions_players(request, body: SessionsPlayersRequest) -> Empty:
    if body.api_key != settings.COOP_API_KEY:
        return Empty()

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
def create_session(
    request: HttpRequest,
    data: CreateSessionRequest,
) -> tuple[int, SuccessResponse] | SuccessResponse:
    if not request.user.is_active or not request.user.is_authenticated:
        return HttpResponseForbidden.status_code, SuccessResponse(success=False, message="not allowed")

    session = SessionModel.objects.create(
        owner=request.user,
        description=data.description,
    )
    session.tags.add(*TagModel.objects.filter(id__in=data.tags).all())
    return SuccessResponse(
        message="session created",
        success=True,
    )

@atomic
def edit_session(
    request: HttpRequest,
    data: EditSessionRequest,
) -> Union[tuple[int, SuccessResponse], SuccessResponse]:
    if not request.user.is_active or not request.user.is_authenticated:
        return HttpResponseForbidden.status_code, SuccessResponse(success=False, message="not allowed")
    try:
        session = SessionModel.objects.get(key=data.id)
    except SessionModel.DoesNotExist:
        return SuccessResponse(success=False, message="session does not exist")
    if session.owner != request.user:
        return SuccessResponse(success=False, message="Not allowed to edit session")
    session.tags.set(TagModel.objects.filter(id__in=data.tags).all())
    session.description = data.description
    session.save()
    return SuccessResponse(message="session updated", success=True)