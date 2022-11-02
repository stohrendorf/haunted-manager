from typing import Union

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.transaction import atomic
from django.http import HttpRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

from haunted_auth.models import ApiKey
from hsutils.viewmodels import (
    CreateSessionRequest,
    DeleteSessionRequest,
    Session,
    SessionAccessRequest,
    SessionsResponse,
    SessionTag,
    SuccessResponse,
    Tag,
    TagsResponse,
)

from .models import Session as SessionModel
from .models import Tag as TagModel


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
            )
            for session in SessionModel.objects.order_by("-created_at").all()
        ],
    )


@login_required
def delete_session(request, body: DeleteSessionRequest) -> Union[tuple[int, SuccessResponse], SuccessResponse]:
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
    if body.api_key != settings.SESSION_CHECK_API_KEY:
        return SuccessResponse(success=False, message="invalid api key")

    try:
        user = get_user_model().objects.get(username=body.username)
    except get_user_model().DoesNotExist:
        return SuccessResponse(success=False, message="user does not exist")
    if not user.is_active:
        return SuccessResponse(success=False, message="user is inactive")
    try:
        auth_token = ApiKey.objects.get(owner=user)
    except ApiKey.DoesNotExist:
        return SuccessResponse(success=False, message="auth token not found")
    if auth_token.key.hex != body.auth_token:
        return SuccessResponse(success=False, message="invalid auth token")
    if not SessionModel.objects.filter(key=body.session_id).exists():
        return SuccessResponse(success=False, message="session does not exist")
    return SuccessResponse(success=True, message="")


@login_required
@atomic
def create_session(
    request: HttpRequest,
    data: CreateSessionRequest,
) -> Union[tuple[int, SuccessResponse], SuccessResponse]:
    session = SessionModel.objects.create(
        owner=request.user,
        description=data.description,
    )
    session.tags.add(*TagModel.objects.filter(id__in=data.tags).all())
    return SuccessResponse(
        message="session created",
        success=True,
    )
