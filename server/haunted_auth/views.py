import logging
from typing import Tuple, Union

import django.contrib.auth
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import (
    HttpRequest,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseRedirect,
    HttpResponseServerError,
)
from django_email_verification import send_email, verify_email_view, verify_token

from haunted_auth.models import ApiKey
from haunted_sessions.models import Session, Tag
from hsutils.viewmodels import (
    CreateSessionRequest,
    Empty,
    LoginRequest,
    ProfileInfoResponse,
    RegisterRequest,
    SuccessResponse,
)

User = get_user_model()


def login(request: HttpRequest, body: LoginRequest) -> Union[SuccessResponse, Tuple[int, SuccessResponse]]:
    user = authenticate(request, username=body.username, password=body.password)
    if user is None or not user.is_active:
        return HttpResponseForbidden.status_code, SuccessResponse(success=False, message="invalid login credentials")

    django_login(request, user)
    logging.info(f"Logged in: {user}")
    print(f"Logged in: {user}")
    return SuccessResponse(success=True, message="")


@login_required
def logout(request: HttpRequest) -> Empty:
    django.contrib.auth.logout(request)
    return Empty()


def profile(request: HttpRequest) -> ProfileInfoResponse:
    if request.user.is_anonymous:
        return ProfileInfoResponse(
            username="anonymous",
            authenticated=False,
            verified=False,
            email=None,
            auth_token=None,
        )

    try:
        key = ApiKey.objects.get(owner=request.user)
    except ApiKey.DoesNotExist:
        key = None
    return ProfileInfoResponse(
        username=request.user.get_username(),
        authenticated=request.user.is_authenticated,
        verified=request.user.is_active,
        email=request.user.email,
        auth_token=key.key.hex if key else None,
    )


def register(request: HttpRequest, body: RegisterRequest) -> Union[tuple[int, SuccessResponse], SuccessResponse]:
    if not request.user.is_anonymous or request.user.is_authenticated:
        return SuccessResponse(success=False, message="already logged in")

    try:
        if User.objects.filter(username=body.username).exists() or User.objects.filter(email=body.email).exists():
            return 409, SuccessResponse(success=False, message="Username and/or email address already in use")
        user = User.objects.create_user(
            is_active=False,
            username=body.username,
            email=body.email,
            password=body.password,
        )
        validate_password(body.password, user)
        user.save()
        send_email(user)
    except ValidationError as e:
        logging.error("registration failed", exc_info=True)
        return HttpResponseBadRequest.status_code, SuccessResponse(success=False, message="; ".join(e.messages))
    except Exception:
        logging.error("registration failed", exc_info=True)
        return HttpResponseServerError.status_code, SuccessResponse(success=False, message="Registration failure")

    return SuccessResponse(success=True, message="registered")


@login_required
def regenerate_token(request: HttpRequest) -> Union[tuple[int, Empty], Empty]:
    try:
        ApiKey.objects.get(owner=request.user).delete()
    except ApiKey.DoesNotExist:
        pass
    request.user.api_key = ApiKey.objects.create(owner=request.user)
    return Empty()


@verify_email_view
def confirm_email_token(request, token):
    verify_token(token)
    return HttpResponseRedirect("/")
