import uuid
from datetime import timedelta
from http import HTTPStatus
from uuid import uuid4

import pytest
from django.test import Client
from django.utils import timezone

from haunted_sessions.models import Session, Tag
from haunted_sessions.views import session_to_response
from hsutils.test_utils import get_test_url, post_test_url
from hsutils.viewmodels import (
    CreateSessionRequest,
    SessionResponse,
    SessionsResponse,
    SuccessResponse,
    TimeSpan,
    session,
    sessions,
)


@pytest.mark.django_db
def test_session_response_conversion(django_user_model):
    user = django_user_model.objects.create_user(
        is_active=True,
        username="username",
        email="test@example.com",
        password="password!!!",
    )
    db_session = Session.objects.create(owner=user, description="description", private=False)
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
    assert converted.time is None
    assert converted.private is False

    time_start = timezone.now()
    time_end = timezone.now() + timedelta(hours=2)
    db_session.start = time_start
    db_session.end = time_end
    db_session.private = True
    db_session.save()
    converted = session_to_response(db_session)
    assert len(converted.tags) == 1
    assert converted.tags[0].name == "tag"
    assert converted.tags[0].description == "tag-description"
    assert converted.owner == "username"
    assert len(converted.players) == 1
    assert converted.players[0] == "username"
    assert converted.id == db_session.key.hex
    assert converted.time is not None
    assert converted.time.start == time_start.isoformat()
    assert converted.time.end == time_end.isoformat()
    assert converted.private is True


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
    db_session = Session.objects.create(owner=user, description="description", private=False)

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
def test_single_session(client: Client, django_user_model):
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
    db_session = Session.objects.create(owner=user, description="description", private=False)

    client.force_login(user)
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
    (session,) = response.sessions
    assert session.description == "description"
    assert session.owner == user.username
    assert len(session.players) == 0
    assert len(session.tags) == 1
    assert session.tags[0].name == "tag"
    assert session.tags[0].description == "tag-description"
    assert session.private is False

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
def test_session_time_sanitization(django_user_model):
    user = django_user_model.objects.create_user(
        is_active=True,
        username="username",
        email="test@example.com",
        password="password!!!",
    )

    db_session = Session.objects.create(owner=user, description="description", private=False)
    assert db_session.start is None
    assert db_session.end is None

    time_start = timezone.now()
    time_end = timezone.now() + timedelta(hours=2)

    db_session.start = time_start
    db_session.save()
    assert db_session.start is None
    assert db_session.end is None

    db_session.end = time_end
    db_session.save()
    assert db_session.start is None
    assert db_session.end is None

    db_session.start = time_start
    db_session.end = time_end
    db_session.save()
    assert db_session.start == time_start
    assert db_session.end == time_end


@pytest.mark.django_db
def test_create_session(client: Client, django_user_model):
    code, response = post_test_url(
        client,
        sessions.path,
        CreateSessionRequest(
            description="session description",
            tags=[],
            time=None,
            private=False,
        ),
        SuccessResponse,
    )
    assert code == HTTPStatus.UNAUTHORIZED
    assert response is not None
    assert response.success is False
    assert Session.objects.count() == 0

    user = django_user_model.objects.create_user(
        is_active=True,
        username="username",
        email="test@example.com",
        password="password!!!",
    )
    Tag.objects.create(name="tag1", description="foo1")
    tag2 = Tag.objects.create(name="tag2", description="foo2")

    start_ts = timezone.now() + timedelta(hours=3)
    end_ts = timezone.now() + timedelta(hours=4)

    client.force_login(user)
    code, response = post_test_url(
        client,
        sessions.path,
        CreateSessionRequest(
            description="session description",
            tags=[tag2.id],
            time=TimeSpan(
                start=start_ts.isoformat(),
                end=end_ts.isoformat(),
            ),
            private=False,
        ),
        SuccessResponse,
    )
    assert code == HTTPStatus.CREATED
    assert response is not None
    assert response.success is True

    (session_object,) = Session.objects.all()
    assert session_object.owner == user
    assert session_object.description == "session description"
    assert list(session_object.tags.all()) == [tag2]
    assert session_object.start == start_ts
    assert session_object.end == end_ts
    assert session_object.players.count() == 0


@pytest.mark.django_db
def test_edit_session(client: Client, django_user_model):
    user = django_user_model.objects.create_user(
        is_active=True,
        username="username",
        email="test@example.com",
        password="password!!!",
    )
    Tag.objects.create(name="tag1", description="foo1")
    tag2 = Tag.objects.create(name="tag2", description="foo2")

    start_ts = timezone.now() + timedelta(hours=3)
    end_ts = timezone.now() + timedelta(hours=4)

    request = CreateSessionRequest(
        description="session description",
        tags=[tag2.id],
        time=TimeSpan(
            start=start_ts.isoformat(),
            end=end_ts.isoformat(),
        ),
        private=False,
    )

    client.force_login(user)
    post_test_url(
        client,
        sessions.path,
        request,
        SuccessResponse,
    )

    code, response = post_test_url(
        client,
        session.path.replace("<str:session_id>", str(uuid4())),
        request,
        SuccessResponse,
    )
    assert code == HTTPStatus.NOT_FOUND
    assert response.success is False

    (session_object,) = Session.objects.all()

    request.description = "changed description"
    request.tags = []
    code, response = post_test_url(
        client,
        session.path.replace("<str:session_id>", str(session_object.key)),
        request,
        SuccessResponse,
    )
    assert code == HTTPStatus.OK
    assert response.success

    (session_object,) = Session.objects.all()
    assert not session_object.tags.all()
    assert session_object.description == "changed description"


@pytest.mark.django_db
def test_single_session_privacy(client: Client, django_user_model):
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
    db_session = Session.objects.create(owner=user, description="description", private=False)

    code, response = get_test_url(
        client,
        "api/v0/sessions/" + db_session.key.hex,
        SessionResponse,
    )
    assert code == HTTPStatus.OK
    assert response is not None
    assert response.session is not None
    assert response.session.id == db_session.key.hex
    assert response.session.private is False

    db_session.private = True
    db_session.save()

    client.logout()
    code, response = get_test_url(
        client,
        "api/v0/sessions/" + db_session.key.hex,
        SessionResponse,
    )

    assert code == HTTPStatus.NOT_FOUND
    assert response.session is None

    client.force_login(user)

    code, response = get_test_url(
        client,
        "api/v0/sessions/" + db_session.key.hex,
        SessionResponse,
    )

    assert code == HTTPStatus.OK
    assert response is not None
    assert response.session is not None
    assert response.session.id == db_session.key.hex
    assert response.session.private is True
