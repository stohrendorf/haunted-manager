import logging
from http import HTTPStatus

import django.contrib.auth
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as django_login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django_email_verification import send_email, verify_email, verify_email_view

from haunted_auth.models import ApiKey
from hsutils.auth import require_authenticated
from hsutils.viewmodels import (
    ChangeEmailRequest,
    ChangePasswordRequest,
    ChangeUsernameRequest,
    Empty,
    LoginRequest,
    ProfileInfoResponse,
    RegisterRequest,
    SuccessResponse,
)

User = get_user_model()


def login(request: HttpRequest, body: LoginRequest) -> SuccessResponse | tuple[int, SuccessResponse]:
    user = authenticate(request, username=body.username, password=body.password)
    if user is None or not user.is_active:
        return HTTPStatus.FORBIDDEN, SuccessResponse(success=False, message="Invalid login credentials")

    django_login(request, user)
    logging.info(f"Logged in: {user}")
    print(f"Logged in: {user}")
    return SuccessResponse(success=True, message="")


@require_authenticated(response=Empty())
def logout(request: HttpRequest) -> Empty | tuple[int, Empty]:
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
            is_staff=False,
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
        is_staff=request.user.is_active and (request.user.is_staff or request.user.is_superuser),
    )


@atomic
def register(request: HttpRequest, body: RegisterRequest) -> tuple[int, SuccessResponse] | SuccessResponse:
    if not request.user.is_anonymous or request.user.is_authenticated:
        return HTTPStatus.BAD_REQUEST, SuccessResponse(success=False, message="already logged in")

    if User.objects.filter(username=body.username).exists() or User.objects.filter(email=body.email).exists():
        return HTTPStatus.CONFLICT, SuccessResponse(
            success=False,
            message="Username and/or email address already in use",
        )

    user = None
    try:
        user = User.objects.create_user(
            is_active=False,
            username=body.username,
            email=body.email,
            password=body.password,
        )
        validate_password(body.password, user)
        ApiKey.objects.create(owner=user)
        user.save()
        send_email(user, thread=not settings.TEST_RUN)
    except ValidationError as e:
        logging.error("registration failed", exc_info=True)
        if user is not None:
            user.delete()
        return HTTPStatus.BAD_REQUEST, SuccessResponse(success=False, message="; ".join(e.messages))
    except Exception:
        logging.error("registration failed", exc_info=True)
        if user is not None:
            user.delete()
        return HTTPStatus.INTERNAL_SERVER_ERROR, SuccessResponse(success=False, message="Registration failure")

    return SuccessResponse(success=True, message="registered")


@require_authenticated(response=Empty())
def regenerate_token(request: HttpRequest) -> tuple[int, Empty] | Empty:
    try:
        ApiKey.objects.get(owner=request.user).delete()
    except ApiKey.DoesNotExist:
        pass
    ApiKey.objects.create(owner=request.user)
    return Empty()


@require_authenticated(response=SuccessResponse(success=False, message="not allowed"))
def change_password(request: HttpRequest, body: ChangePasswordRequest) -> SuccessResponse | tuple[int, SuccessResponse]:
    try:
        validate_password(body.password, request.user)
    except ValidationError as e:
        return HTTPStatus.BAD_REQUEST, SuccessResponse(
            success=False,
            message="Your new password is not secure enough for the following reasons:\n" + "\n".join(e.messages),
        )

    request.user.set_password(body.password)
    request.user.save()
    return SuccessResponse(success=True, message="password changed")


@atomic
@require_authenticated(response=SuccessResponse(success=False, message="not allowed"))
def change_username(request: HttpRequest, body: ChangeUsernameRequest) -> SuccessResponse | tuple[int, SuccessResponse]:
    if User.objects.filter(username=body.username).exists():
        return HTTPStatus.CONFLICT, SuccessResponse(success=False, message="Username already in use")

    try:
        request.user.username = body.username
    except Exception:
        logging.error("failed to change username", exc_info=True)
        return HTTPStatus.INTERNAL_SERVER_ERROR, SuccessResponse(success=False, message="Failed to change username")

    request.user.username = body.username
    request.user.save()
    return SuccessResponse(success=True, message="username changed")


@require_authenticated(response=SuccessResponse(success=False, message="not allowed"))
def change_email(request: HttpRequest, body: ChangeEmailRequest) -> SuccessResponse | tuple[int, SuccessResponse]:
    if User.objects.filter(email=body.email).exists():
        return HTTPStatus.CONFLICT, SuccessResponse(success=False, message="Email address already in use.")

    request.user.email = body.email
    request.user.save()
    return SuccessResponse(success=True, message="email changed")


@verify_email_view
def confirm_email_token(request: HttpRequest, token: str) -> HttpResponse:
    verify_email(token)
    return HttpResponseRedirect("/")
