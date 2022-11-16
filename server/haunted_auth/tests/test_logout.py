from http import HTTPStatus

import pytest
from django.contrib.auth.models import AbstractUser
from django.test import Client

from hsutils.test_utils import get_test_url
from hsutils.viewmodels import Empty, logout


@pytest.mark.django_db
def test_logout(client: Client, django_user_model):
    assert django_user_model.objects.count() == 0

    code, response = get_test_url(
        client,
        logout.path,
        Empty,
    )
    assert code == HTTPStatus.UNAUTHORIZED
    assert response is not None
    user: AbstractUser = django_user_model.objects.create_user(
        is_active=False,
        username="username",
        email="test@example.com",
        password="password!!!",
    )
    code, response = get_test_url(
        client,
        logout.path,
        Empty,
    )
    assert code == HTTPStatus.UNAUTHORIZED
    assert response is not None

    user.is_active = True
    user.save()
    client.force_login(user)
    code, response = get_test_url(
        client,
        logout.path,
        Empty,
    )
    assert code == HTTPStatus.OK
    assert response is not None
