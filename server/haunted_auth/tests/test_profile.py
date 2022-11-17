import uuid
from http import HTTPStatus

import pytest
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMessage
from django.test import Client
from test_user_registration import try_register

from hsutils.test_utils import get_test_url, post_test_url
from hsutils.viewmodels import (
    ChangeEmailRequest,
    ChangePasswordRequest,
    ChangeUsernameRequest,
    ProfileInfoResponse,
    SuccessResponse,
    change_email,
    change_password,
    change_username,
    profile,
)


@pytest.mark.django_db
def test_profile_anonymous(client: Client, django_user_model):
    assert django_user_model.objects.count() == 0
    code, response = get_test_url(client, profile.path, ProfileInfoResponse)
    assert code == HTTPStatus.OK
    assert response is not None
    assert response.email is None
    assert response.authenticated is False
    assert response.verified is False


@pytest.mark.django_db
def test_profile_registered(client: Client, django_user_model):
    assert django_user_model.objects.count() == 0
    user = django_user_model.objects.create_user(
        username="user",
        email="user@example.com",
        password="password123",
    )
    user.is_active = True
    user.save()
    client.force_login(user)
    code, response = get_test_url(client, profile.path, ProfileInfoResponse)
    assert code == HTTPStatus.OK
    assert response is not None
    assert response.email == "user@example.com"
    assert response.authenticated is True
    assert response.verified is True


@pytest.mark.django_db
def test_change_password(
    client: Client,
    django_user_model: type[AbstractUser],
    mailoutbox: list[EmailMessage],
):
    code, response = post_test_url(
        client,
        change_password.path,
        ChangePasswordRequest(password="password987"),
        SuccessResponse,
    )
    assert code == HTTPStatus.UNAUTHORIZED
    assert response is not None
    assert response.success is False
    assert len(mailoutbox) == 0

    try_register(
        client,
        email="test@example.com",
        password=uuid.uuid4().hex,
        username="test-user",
    )
    user: AbstractUser = django_user_model.objects.get()
    user.save()
    mailoutbox.clear()

    client.force_login(user)
    code, response = post_test_url(
        client,
        change_password.path,
        ChangePasswordRequest(password="password987"),
        SuccessResponse,
    )
    assert code == HTTPStatus.UNAUTHORIZED
    assert response is not None
    assert response.success is False
    assert len(mailoutbox) == 0

    user.is_active = True
    user.save()

    client.force_login(user)
    code, response = post_test_url(
        client,
        change_password.path,
        ChangePasswordRequest(password="password987"),
        SuccessResponse,
    )
    assert code == HTTPStatus.OK
    assert response is not None
    assert response.success is True
    assert len(mailoutbox) == 0

    user = django_user_model.objects.get()
    client.force_login(user)
    code, response = post_test_url(
        client,
        change_password.path,
        ChangePasswordRequest(password="123"),
        SuccessResponse,
    )
    assert code == HTTPStatus.BAD_REQUEST
    assert response is not None
    assert response.success is False
    assert len(mailoutbox) == 0


@pytest.mark.django_db
def test_change_username(
    client: Client,
    django_user_model: type[AbstractUser],
    mailoutbox: list[EmailMessage],
):
    code, response = post_test_url(
        client,
        change_username.path,
        ChangeUsernameRequest(username="test-user-2"),
        SuccessResponse,
    )
    assert code == HTTPStatus.UNAUTHORIZED
    assert response is not None
    assert response.success is False
    assert len(mailoutbox) == 0

    try_register(
        client,
        email="test@example.com",
        password=uuid.uuid4().hex,
        username="test-user",
    )
    user: AbstractUser = django_user_model.objects.get()
    user.save()
    mailoutbox.clear()

    client.force_login(user)
    code, response = post_test_url(
        client,
        change_username.path,
        ChangeUsernameRequest(username="test-user-2"),
        SuccessResponse,
    )
    assert code == HTTPStatus.UNAUTHORIZED
    assert response is not None
    assert response.success is False
    assert len(mailoutbox) == 0

    user.is_active = True
    user.save()

    client.force_login(user)
    code, response = post_test_url(
        client,
        change_username.path,
        ChangeUsernameRequest(username="test-user-2"),
        SuccessResponse,
    )
    assert code == HTTPStatus.OK
    assert response is not None
    assert response.success is True
    assert len(mailoutbox) == 0

    client.force_login(user)
    code, response = post_test_url(
        client,
        change_username.path,
        ChangeUsernameRequest(username="test-user-2"),
        SuccessResponse,
    )
    assert code == HTTPStatus.CONFLICT
    assert response is not None
    assert response.success is False
    assert len(mailoutbox) == 0


@pytest.mark.django_db
def test_change_email(
    client: Client,
    django_user_model: type[AbstractUser],
    mailoutbox: list[EmailMessage],
):
    code, response = post_test_url(
        client,
        change_email.path,
        ChangeEmailRequest(email="test-2@example.com"),
        SuccessResponse,
    )
    assert code == HTTPStatus.UNAUTHORIZED
    assert response is not None
    assert response.success is False
    assert len(mailoutbox) == 0

    try_register(
        client,
        email="test@example.com",
        password=uuid.uuid4().hex,
        username="test-user",
    )
    user: AbstractUser = django_user_model.objects.get()
    user.save()
    mailoutbox.clear()

    client.force_login(user)
    code, response = post_test_url(
        client,
        change_email.path,
        ChangeEmailRequest(email="test-2@example.com"),
        SuccessResponse,
    )
    assert code == HTTPStatus.UNAUTHORIZED
    assert response is not None
    assert response.success is False
    assert len(mailoutbox) == 0

    user.is_active = True
    user.save()

    client.force_login(user)
    code, response = post_test_url(
        client,
        change_email.path,
        ChangeEmailRequest(email="test-2@example.com"),
        SuccessResponse,
    )
    assert code == HTTPStatus.OK
    assert response is not None
    assert response.success is True
    assert len(mailoutbox) == 0

    client.force_login(user)
    code, response = post_test_url(
        client,
        change_email.path,
        ChangeEmailRequest(email="test-2@example.com"),
        SuccessResponse,
    )
    assert code == HTTPStatus.CONFLICT
    assert response is not None
    assert response.success is False
    assert len(mailoutbox) == 0
