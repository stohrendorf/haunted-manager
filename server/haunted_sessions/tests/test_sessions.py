import uuid
from http import HTTPStatus

import pytest
from django.test import Client

from haunted_sessions.models import Session, Tag
from haunted_sessions.views import session_to_response
from hsutils.test_utils import get_test_url
from hsutils.viewmodels import SessionResponse, SessionsResponse, sessions


@pytest.mark.django_db
def test_session_response_conversion(django_user_model):
    user = django_user_model.objects.create_user(
        is_active=True,
        username="username",
        email="test@example.com",
        password="password!!!",
    )
    db_session = Session.objects.create(owner=user, description="description")
    tag = Tag.objects.create(name="tag", description="tag-description")
    db_session.tags.add(tag)
    db_session.players.add(user)
    db_session.save()

    converted = session_to_response(db_session)
    assert len(converted.tags) == 1
    assert converted.tags[0].name == "tag"
    assert converted.tags[0].description == "tag-description"
    assert converted.owner == "username"
    assert len(converted.players) == 1
    assert converted.players[0] == "username"
    assert converted.id == db_session.key.hex


@pytest.mark.django_db
def test_sessions_list(client: Client, django_user_model):
    code, response = get_test_url(
        client,
        sessions.path,
        SessionsResponse,
    )
    assert code == HTTPStatus.OK
    assert response is not None
    assert len(response.sessions) == 0

    assert django_user_model.objects.count() == 0
    user = django_user_model.objects.create_user(
        is_active=True,
        username="username",
        email="test@example.com",
        password="password!!!",
    )
    db_session = Session.objects.create(owner=user, description="description")

    code, response = get_test_url(
        client,
        sessions.path,
        SessionsResponse,
    )
    assert code == HTTPStatus.OK
    assert response is not None
    assert len(response.sessions) == 1
    (session,) = response.sessions
    assert session.description == "description"
    assert session.owner == user.username
    assert len(session.players) == 0
    assert len(session.tags) == 0

    tag = Tag.objects.create(name="tag", description="tag-description")
    db_session.tags.add(tag)
    db_session.save()

    code, response = get_test_url(
        client,
        sessions.path,
        SessionsResponse,
    )
    assert code == HTTPStatus.OK
    assert response is not None
    assert len(response.sessions) == 1
    (session,) = response.sessions
    assert session.description == "description"
    assert session.owner == user.username
    assert len(session.players) == 0
    assert len(session.tags) == 1
    assert session.tags[0].name == "tag"
    assert session.tags[0].description == "tag-description"

    db_session.players.add(user)
    db_session.save()

    code, response = get_test_url(
        client,
        sessions.path,
        SessionsResponse,
    )
    assert code == HTTPStatus.OK
    assert response is not None
    assert len(response.sessions) == 1
    (session,) = response.sessions
    assert session.description == "description"
    assert session.owner == user.username
    assert len(session.players) == 1
    assert session.players[0] == "username"
    assert len(session.tags) == 1
    assert session.tags[0].name == "tag"
    assert session.tags[0].description == "tag-description"


@pytest.mark.django_db
def test_session(client: Client, django_user_model):
    code, response = get_test_url(
        client,
        "api/v0/sessions/" + uuid.uuid4().hex,
        SessionResponse,
    )
    assert code == HTTPStatus.NOT_FOUND
    assert response is not None
    assert response.session is None

    assert django_user_model.objects.count() == 0
    user = django_user_model.objects.create_user(
        is_active=True,
        username="username",
        email="test@example.com",
        password="password!!!",
    )
    db_session = Session.objects.create(owner=user, description="description")

    code, response = get_test_url(
        client,
        "api/v0/sessions/" + db_session.key.hex,
        SessionResponse,
    )
    assert code == HTTPStatus.OK
    assert response is not None
    assert response.session is not None
    assert response.session.id == db_session.key.hex

    tag = Tag.objects.create(name="tag", description="tag-description")
    db_session.tags.add(tag)
    db_session.save()

    code, response = get_test_url(
        client,
        sessions.path,
        SessionsResponse,
    )
    assert code == HTTPStatus.OK
    assert response is not None
    assert len(response.sessions) == 1
    (s,) = response.sessions
    assert s.description == "description"
    assert s.owner == user.username
    assert len(s.players) == 0
    assert len(s.tags) == 1
    assert s.tags[0].name == "tag"
    assert s.tags[0].description == "tag-description"

    db_session.players.add(user)
    db_session.save()

    code, response = get_test_url(
        client,
        sessions.path,
        SessionsResponse,
    )
    assert code == HTTPStatus.OK
    assert response is not None
    assert len(response.sessions) == 1
    (s,) = response.sessions
    assert s.description == "description"
    assert s.owner == user.username
    assert len(s.players) == 1
    assert s.players[0] == "username"
    assert len(s.tags) == 1
    assert s.tags[0].name == "tag"
    assert s.tags[0].description == "tag-description"