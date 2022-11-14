import uuid
from typing import Optional

import pytest
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponse, HttpResponseBadRequest
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
def test_register_verify_happy_path(client: Client, django_user_model):
    code, response = try_register(
        client,
        email="test@example.com",
        password=uuid.uuid4().hex,
        username="test-user",
    )
    assert code == HttpResponse.status_code
    assert response is not None
    assert response.success is True

    user: AbstractUser = django_user_model.objects.get()
    assert user.is_active is False
    assert user.email == "test@example.com"
    assert user.get_username() == "test-user"

    # check that a duplicate user can't be registered

    code, response = try_register(
        client,
        email="test@example.com",
        password=uuid.uuid4().hex,
        username="test-user",
    )
    assert code == 409
    assert response is not None
    assert response.success is False

    user = django_user_model.objects.get()
    assert user.is_active is False
    assert user.email == "test@example.com"
    assert user.get_username() == "test-user"


@pytest.mark.django_db
def test_register_missing_data(client: Client, django_user_model):
    # TODO these error checks are stupid, a proper exception handling is needed
    code, response = try_register(client, email="", password=uuid.uuid4().hex, username="test-user")
    assert code == 500
    assert response is None
    assert django_user_model.objects.count() == 0

    code, response = try_register(client, email="test@example.com", password="", username="test-user")
    assert code == 500
    assert response is None
    assert django_user_model.objects.count() == 0

    code, response = try_register(client, email="test@example.com", password=uuid.uuid4().hex, username="")
    assert code == 500
    assert response is None
    assert django_user_model.objects.count() == 0


@pytest.mark.django_db
def test_register_invalid_password(client: Client, django_user_model):
    code, response = try_register(client, email="test@example.com", password="1234", username="test-user")
    assert code == HttpResponseBadRequest.status_code
    assert response is not None
    assert response.success is False
    assert response.message is not None
    assert django_user_model.objects.count() == 0
