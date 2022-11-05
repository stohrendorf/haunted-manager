import logging

import django.contrib.auth
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.http import (
    HttpRequest,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseRedirect,
    HttpResponseServerError,
)
from django_email_verification import send_email, verify_email_view, verify_token

from haunted_auth.models import ApiKey
from hsutils.viewmodels import (
    ChangeEmailRequest,
    ChangePasswordRequest,
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
        return HttpResponseForbidden.status_code, SuccessResponse(success=False, message="Invalid login credentials")

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


@atomic
def register(request: HttpRequest, body: RegisterRequest) -> tuple[int, SuccessResponse] | SuccessResponse:
    if not request.user.is_anonymous or request.user.is_authenticated:
        return SuccessResponse(success=False, message="already logged in")

    if User.objects.filter(username=body.username).exists() or User.objects.filter(email=body.email).exists():
        return 409, SuccessResponse(success=False, message="Username and/or email address already in use")

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
        send_email(user)
    except ValidationError as e:
        logging.error("registration failed", exc_info=True)
        if user is not None:
            user.delete()
        return HttpResponseBadRequest.status_code, SuccessResponse(success=False, message="; ".join(e.messages))
    except Exception:
        logging.error("registration failed", exc_info=True)
        if user is not None:
            user.delete()
        return HttpResponseServerError.status_code, SuccessResponse(success=False, message="Registration failure")

    return SuccessResponse(success=True, message="registered")


@login_required
def regenerate_token(request: HttpRequest) -> tuple[int, Empty] | Empty:
    try:
        ApiKey.objects.get(owner=request.user).delete()
    except ApiKey.DoesNotExist:
        pass
    ApiKey.objects.create(owner=request.user)
    return Empty()


@login_required
def change_password(request: HttpRequest, body: ChangePasswordRequest) -> SuccessResponse:
    try:
        validate_password(body.password, request.user)
    except ValidationError as e:
        return SuccessResponse(
            success=False,
            message="Your new password is not secure enough for the following reasons:\n" + "\n".join(e.messages),
        )

    request.user.set_password(body.password)
    request.user.save()
    return SuccessResponse(success=True, message="password changed")


@login_required
def change_email(request: HttpRequest, body: ChangeEmailRequest) -> SuccessResponse:
    if User.objects.filter(email=body.email).exists():
        return SuccessResponse(success=False, message="Email address already in use.")

    request.user.email = body.email
    request.user.save()
    send_email(request.user)
    return SuccessResponse(success=True, message="email changed")


@verify_email_view
def confirm_email_token(request, token):
    verify_token(token)
    return HttpResponseRedirect("/")
