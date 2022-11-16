from http import HTTPStatus

import pytest
from django.contrib.auth.models import AbstractUser
from django.test import Client

from hsutils.test_utils import post_test_url
from hsutils.viewmodels import LoginRequest, SuccessResponse, login


@pytest.mark.django_db
def test_login(client: Client, django_user_model):
    assert django_user_model.objects.count() == 0

    code, response = post_test_url(
        client,
        login.path,
        LoginRequest(password="password!!!", username="username"),
        SuccessResponse,
    )
    assert code == HTTPStatus.FORBIDDEN
    assert response is not None
    assert response.success is False
    user: AbstractUser = django_user_model.objects.create_user(
        is_active=False,
        username="username",
        email="test@example.com",
        password="password!!!",
    )
    code, response = post_test_url(
        client,
        login.path,
        LoginRequest(password="password!!!", username="username"),
        SuccessResponse,
    )
    assert code == HTTPStatus.FORBIDDEN
    assert response is not None
    assert response.success is False

    user.is_active = True
    user.save()
    code, response = post_test_url(
        client,
        login.path,
        LoginRequest(password="password!!!", username="username"),
        SuccessResponse,
    )
    assert code == HTTPStatus.OK
    assert response is not None
    assert response.success is True

    code, response = post_test_url(
        client,
        login.path,
        LoginRequest(password="password", username="username"),
        SuccessResponse,
    )
    assert code == HTTPStatus.FORBIDDEN
    assert response is not None
    assert response.success is False

    code, response = post_test_url(
        client,
        login.path,
        LoginRequest(password="password!!!", username="xxx"),
        SuccessResponse,
    )
    assert code == HTTPStatus.FORBIDDEN
    assert response is not None
    assert response.success is False
