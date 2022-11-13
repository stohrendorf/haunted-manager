import pytest
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponseBase, HttpResponseForbidden
from pytest_django.live_server_helper import LiveServer

from hsutils.test_utils import post_test_url
from hsutils.viewmodels import LoginRequest, SuccessResponse, login


@pytest.mark.django_db
def test_login(live_server: LiveServer, django_user_model):
    assert django_user_model.objects.count() == 0

    code, response = post_test_url(
        live_server,
        login.path,
        LoginRequest(password="password!!!", username="username"),
        SuccessResponse,
    )
    assert code == HttpResponseForbidden.status_code
    assert response is not None
    assert response.success is False
    user: AbstractUser = django_user_model.objects.create_user(
        is_active=False,
        username="username",
        email="test@example.com",
        password="password!!!",
    )
    code, response = post_test_url(
        live_server,
        login.path,
        LoginRequest(password="password!!!", username="username"),
        SuccessResponse,
    )
    assert code == HttpResponseForbidden.status_code
    assert response is not None
    assert response.success is False

    user.is_active = True
    user.save()
    code, response = post_test_url(
        live_server,
        login.path,
        LoginRequest(password="password!!!", username="username"),
        SuccessResponse,
    )
    assert code == HttpResponseBase.status_code
    assert response is not None
    assert response.success is True

    code, response = post_test_url(
        live_server,
        login.path,
        LoginRequest(password="password", username="username"),
        SuccessResponse,
    )
    assert code == HttpResponseForbidden.status_code
    assert response is not None
    assert response.success is False

    code, response = post_test_url(
        live_server,
        login.path,
        LoginRequest(password="password!!!", username="xxx"),
        SuccessResponse,
    )
    assert code == HttpResponseForbidden.status_code
    assert response is not None
    assert response.success is False
