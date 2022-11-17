import uuid
from email.message import EmailMessage
from http import HTTPStatus
from typing import Optional

import pytest
from django.contrib.auth.models import AbstractUser
from django.test import Client

from hsutils.test_utils import post_test_url
from hsutils.viewmodels import RegisterRequest, SuccessResponse, register


def try_register(
    client: Client,
    email: str,
    password: str,
    username: str,
) -> tuple[int, Optional[SuccessResponse]]:
    return post_test_url(
        client,
        register.path,
        RegisterRequest(email=email, password=password, username=username),
        SuccessResponse,
    )


@pytest.mark.django_db
def test_register_verify_happy_path(
    client: Client,
    django_user_model: type[AbstractUser],
    mailoutbox: list[EmailMessage],
):
    code, response = try_register(
        client,
        email="test@example.com",
        password=uuid.uuid4().hex,
        username="test-user",
    )
    assert code == HTTPStatus.OK
    assert response is not None
    assert response.success is True
    assert len(mailoutbox) == 1

    mailoutbox.clear()

    user: AbstractUser = django_user_model.objects.get()
    assert user.is_active is False
    assert user.email == "test@example.com"
    assert user.get_username() == "test-user"
    assert len(mailoutbox) == 0


@pytest.mark.django_db
def test_register_logged_in(
    client: Client,
    django_user_model: type[AbstractUser],
    mailoutbox: list[EmailMessage],
):
    code, response = try_register(
        client,
        email="test@example.com",
        password=uuid.uuid4().hex,
        username="test-user",
    )
    assert code == HTTPStatus.OK
    assert response is not None
    assert response.success is True
    assert len(mailoutbox) == 1

    mailoutbox.clear()

    user: AbstractUser = django_user_model.objects.get()
    user.is_active = True
    user.save()
    client.force_login(user)
    code, response = try_register(
        client,
        email="test@example.com",
        password=uuid.uuid4().hex,
        username="test-user",
    )
    assert code == HTTPStatus.BAD_REQUEST
    assert response is not None
    assert response.success is False
    assert len(mailoutbox) == 0


@pytest.mark.django_db
def test_register_duplicate(
    client: Client,
    mailoutbox: list[EmailMessage],
):
    try_register(
        client,
        email="test@example.com",
        password=uuid.uuid4().hex,
        username="test-user",
    )
    mailoutbox.clear()

    code, response = try_register(
        client,
        email="test@example.com",
        password=uuid.uuid4().hex,
        username="test-user",
    )
    assert code == 409
    assert response is not None
    assert response.success is False
    assert len(mailoutbox) == 0


@pytest.mark.django_db
def test_register_duplicate_username(
    client: Client,
    mailoutbox: list[EmailMessage],
):
    try_register(
        client,
        email="test@example.com",
        password=uuid.uuid4().hex,
        username="test-user",
    )
    mailoutbox.clear()

    code, response = try_register(
        client,
        email="test-2@example.com",
        password=uuid.uuid4().hex,
        username="test-user",
    )
    assert code == 409
    assert response is not None
    assert response.success is False
    assert len(mailoutbox) == 0


@pytest.mark.django_db
def test_register_duplicate_email(
    client: Client,
    mailoutbox: list[EmailMessage],
):
    try_register(
        client,
        email="test@example.com",
        password=uuid.uuid4().hex,
        username="test-user",
    )
    mailoutbox.clear()

    code, response = try_register(
        client,
        email="test@example.com",
        password=uuid.uuid4().hex,
        username="test-user-2",
    )
    assert code == 409
    assert response is not None
    assert response.success is False
    assert len(mailoutbox) == 0


@pytest.mark.django_db
def test_register_missing_data(client: Client, django_user_model: type[AbstractUser], mailoutbox: list[EmailMessage]):
    # TODO these error checks are stupid, a proper exception handling is needed
    code, response = try_register(client, email="", password=uuid.uuid4().hex, username="test-user")
    assert code == HTTPStatus.BAD_REQUEST
    assert response is None
    assert django_user_model.objects.count() == 0
    assert len(mailoutbox) == 0

    code, response = try_register(client, email="test@example.com", password="", username="test-user")
    assert code == HTTPStatus.BAD_REQUEST
    assert response is None
    assert django_user_model.objects.count() == 0
    assert len(mailoutbox) == 0

    code, response = try_register(client, email="test@example.com", password=uuid.uuid4().hex, username="")
    assert code == HTTPStatus.BAD_REQUEST
    assert response is None
    assert django_user_model.objects.count() == 0
    assert len(mailoutbox) == 0


@pytest.mark.django_db
def test_register_invalid_password(
    client: Client,
    django_user_model: type[AbstractUser],
    mailoutbox: list[EmailMessage],
):
    code, response = try_register(client, email="test@example.com", password="1234", username="test-user")
    assert code == HTTPStatus.BAD_REQUEST
    assert response is not None
    assert response.success is False
    assert response.message is not None
    assert django_user_model.objects.count() == 0
    assert len(mailoutbox) == 0
