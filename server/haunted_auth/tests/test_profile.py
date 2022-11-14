import pytest
from django.http import HttpResponse
from django.test import Client

from hsutils.test_utils import get_test_url
from hsutils.viewmodels import ProfileInfoResponse, profile


@pytest.mark.django_db
def test_profile_anonymous(client: Client, django_user_model):
    assert django_user_model.objects.count() == 0
    code, response = get_test_url(client, profile.path, ProfileInfoResponse)
    assert code == HttpResponse.status_code
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
    assert code == HttpResponse.status_code
    assert response is not None
    assert response.email == "user@example.com"
    assert response.authenticated is True
    assert response.verified is True
