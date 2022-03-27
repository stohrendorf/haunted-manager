import uuid

import pytest
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from pytest_django.live_server_helper import LiveServer

from hsutils.test_utils import get_test_url, post_test_url
from hsutils.viewmodels import (
    ProfileInfoResponse,
    RegisterRequest,
    SuccessResponse,
    get_profile,
    register,
)


@pytest.mark.django_db
def test_not_registered(live_server: LiveServer):
    assert get_user_model().objects.count() == 0
    code, response = get_test_url(live_server, get_profile.path, ProfileInfoResponse)
    assert code == HttpResponse.status_code
    assert response.email is None
    assert response.authenticated is False


@pytest.mark.django_db
def test_register_verify_happy_path(live_server: LiveServer):
    code, response = post_test_url(
        live_server,
        register.path,
        RegisterRequest(email="test@example.com", password=uuid.uuid4().hex, username="test-user"),
        SuccessResponse,
    )
    assert code == HttpResponse.status_code
    assert response.success is True

    user = get_user_model().objects.get()
    assert user.is_active is False
    assert user.email == "test@example.com"
    assert user.get_username() == "test-user"

    code, response = post_test_url(
        live_server,
        register.path,
        RegisterRequest(email="test@example.com", password=uuid.uuid4().hex, username="test-user"),
        SuccessResponse,
    )
    assert code == 409
    assert response.success is False

    user = get_user_model().objects.get()
    assert user.is_active is False
    assert user.email == "test@example.com"
    assert user.get_username() == "test-user"


@pytest.mark.django_db
def test_register_invalid_data(live_server: LiveServer):
    # TODO these error checks are stupid, a proper exception handling is needed
    code, response = post_test_url(
        live_server,
        register.path,
        RegisterRequest(email="", password=uuid.uuid4().hex, username="test-user"),
        SuccessResponse,
    )
    assert code == 500
    assert response is None
    assert get_user_model().objects.count() == 0

    code, response = post_test_url(
        live_server,
        register.path,
        RegisterRequest(email="test@example.com", password="", username="test-user"),
        SuccessResponse,
    )
    assert code == 500
    assert response is None
    assert get_user_model().objects.count() == 0

    code, response = post_test_url(
        live_server,
        register.path,
        RegisterRequest(email="test@example.com", password=uuid.uuid4().hex, username=""),
        SuccessResponse,
    )
    assert code == 500
    assert response is None
    assert get_user_model().objects.count() == 0
