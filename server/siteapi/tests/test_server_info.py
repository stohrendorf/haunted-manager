from http import HTTPStatus

import pytest
from django.conf import settings
from django.test import Client

from haunted_sessions.models import Session
from hsutils.test_utils import get_test_url
from hsutils.viewmodels import ServerInfoResponse, server_info


@pytest.mark.django_db
def test_server_info(client: Client, django_user_model):
    assert django_user_model.objects.count() == 0
    assert Session.objects.count() == 0

    code, response = get_test_url(client, server_info.path, ServerInfoResponse)
    assert code == HTTPStatus.OK
    assert response is not None
    assert response.coop_url == settings.COOP_SERVER_URL
    assert response.total_sessions == 0
    assert response.total_users == 0

    user = django_user_model.objects.create_user(
        username="user",
        email="user@example.com",
        password="password123",
    )
    code, response = get_test_url(client, server_info.path, ServerInfoResponse)
    assert code == HTTPStatus.OK
    assert response is not None
    assert response.coop_url == settings.COOP_SERVER_URL
    assert response.total_sessions == 0
    assert response.total_users == 1

    for _ in range(3):
        Session.objects.create(owner=user, description="", private=False)
    code, response = get_test_url(client, server_info.path, ServerInfoResponse)
    assert code == HTTPStatus.OK
    assert response is not None
    assert response.coop_url == settings.COOP_SERVER_URL
    assert response.total_sessions == 3
    assert response.total_users == 1
