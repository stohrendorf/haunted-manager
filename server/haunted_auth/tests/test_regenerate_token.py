import pytest
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponseBase, HttpResponseForbidden
from django.test import Client

from hsutils.test_utils import get_test_url
from hsutils.viewmodels import Empty, regenerate_token


@pytest.mark.django_db
def test_regenerate_token(client: Client, django_user_model):
    assert django_user_model.objects.count() == 0

    code, response = get_test_url(
        client,
        regenerate_token.path,
        Empty,
    )
    assert code == HttpResponseForbidden.status_code
    assert response is not None

    user: AbstractUser = django_user_model.objects.create_user(
        is_active=False,
        username="username",
        email="test@example.com",
        password="password!!!",
    )
    code, response = get_test_url(
        client,
        regenerate_token.path,
        Empty,
    )
    assert code == HttpResponseForbidden.status_code
    assert response is not None

    user.is_active = True
    user.save()
    client.force_login(user)
    code, response = get_test_url(
        client,
        regenerate_token.path,
        Empty,
    )
    assert code == HttpResponseBase.status_code
    assert response is not None
