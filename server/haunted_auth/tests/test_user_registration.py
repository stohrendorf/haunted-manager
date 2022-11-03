import uuid
from typing import Optional

import pytest
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseBadRequest
from pytest_django.live_server_helper import LiveServer

from hsutils.test_utils import get_test_url, post_test_url
from hsutils.viewmodels import (
    ProfileInfoResponse,
    RegisterRequest,
    SuccessResponse,
    get_profile,
    register,
)


def try_register(
    live_server: LiveServer,
    email: str,
    password: str,
    username: str,
) -> tuple[int, Optional[SuccessResponse]]:
    return post_test_url(
        live_server,
        register.path,
        RegisterRequest(email=email, password=password, username=username),
        SuccessResponse,
    )


@pytest.mark.django_db
def test_not_registered(live_server: LiveServer):
    assert get_user_model().objects.count() == 0
    code, response = get_test_url(live_server, get_profile.path, ProfileInfoResponse)
    assert code == HttpResponse.status_code
    assert response is not None
    assert response.email is None
    assert response.authenticated is False


@pytest.mark.django_db
def test_register_verify_happy_path(live_server: LiveServer):
    code, response = try_register(
        live_server, email="test@example.com", password=uuid.uuid4().hex, username="test-user"
    )
    assert code == HttpResponse.status_code
    assert response is not None
    assert response.success is True

    user = get_user_model().objects.get()
    assert user.is_active is False
    assert user.email == "test@example.com"
    assert user.get_username() == "test-user"

    # check that a duplicate user can't be registered

    code, response = try_register(
        live_server, email="test@example.com", password=uuid.uuid4().hex, username="test-user"
    )
    assert code == 409
    assert response.success is False

    user = get_user_model().objects.get()
    assert user.is_active is False
    assert user.email == "test@example.com"
    assert user.get_username() == "test-user"


@pytest.mark.django_db
def test_register_missing_data(live_server: LiveServer):
    # TODO these error checks are stupid, a proper exception handling is needed
    code, response = try_register(live_server, email="", password=uuid.uuid4().hex, username="test-user")
    assert code == 500
    assert response is None
    assert get_user_model().objects.count() == 0

    code, response = try_register(live_server, email="test@example.com", password="", username="test-user")
    assert code == 500
    assert response is None
    assert get_user_model().objects.count() == 0

    code, response = try_register(live_server, email="test@example.com", password=uuid.uuid4().hex, username="")
    assert code == 500
    assert response is None
    assert get_user_model().objects.count() == 0


@pytest.mark.django_db
def test_register_invalid_password(live_server: LiveServer):
    code, response = try_register(live_server, email="test@example.com", password="1234", username="test-user")
    assert code == HttpResponseBadRequest.status_code
    assert response is not None
    assert response.success is False
    assert response.message is not None
    assert get_user_model().objects.count() == 0
