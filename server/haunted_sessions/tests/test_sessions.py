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
    assert converted.owner == user.username
    assert len(converted.players) == 1
    assert converted.players[0] == user.username
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
    assert converted.owner == user.username
    assert len(converted.players) == 1
    assert converted.players[0] == user.username
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
    assert session.players[0] == user.username
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
    private_user = django_user_model.objects.create_user(
        is_active=True,
        username="private",
        email="private@example.com",
        password="password!!!",
    )
    super_user = django_user_model.objects.create_user(
        is_active=True,
        username="admin",
        email="admin@example.com",
        password="password!!!",
    )
    super_user.is_staff = True
    super_user.save()
    db_session_public = Session.objects.create(owner=super_user, description="description", private=False)
    db_session_private = Session.objects.create(owner=private_user, description="description", private=True)

    # normal user only sees his the public session
    client.force_login(user)
    code, response = get_test_url(
        client,
        sessions.path,
        SessionsResponse,
    )
    assert code == HTTPStatus.OK
    assert response is not None
    assert len(response.sessions) == 1

    code, response = get_test_url(
        client,
        "api/v0/sessions/" + db_session_private.key.hex,
        SessionResponse,
    )
    assert code == HTTPStatus.NOT_FOUND
    assert response is not None
    assert response.session is None

    # private user sees the public session and the private session
    client.force_login(private_user)
    code, response = get_test_url(
        client,
        sessions.path,
        SessionsResponse,
    )
    assert code == HTTPStatus.OK
    assert response is not None
    assert len(response.sessions) == 2

    for db_session in (db_session_public, db_session_private):
        code, response = get_test_url(
            client,
            "api/v0/sessions/" + db_session.key.hex,
            SessionResponse,
        )
        assert code == HTTPStatus.OK
        assert response is not None
        assert response.session is not None

    # admin/staff can see all sessions
    client.force_login(super_user)
    code, response = get_test_url(
        client,
        sessions.path,
        SessionsResponse,
    )
    assert code == HTTPStatus.OK
    assert response is not None
    assert len(response.sessions) == 2

    for db_session in (db_session_public, db_session_private):
        code, response = get_test_url(
            client,
            "api/v0/sessions/" + db_session.key.hex,
            SessionResponse,
        )
        assert code == HTTPStatus.OK
        assert response is not None
        assert response.session is not None

    # verify that the normal user gets his session data
    client.force_login(user)
    code, response = get_test_url(
        client,
        "api/v0/sessions/" + db_session_public.key.hex,
        SessionResponse,
    )
    assert code == HTTPStatus.OK
    assert response is not None
    assert response.session is not None
    assert response.session.id == db_session_public.key.hex

    tag = Tag.objects.create(name="tag", description="tag-description")
    db_session_public.tags.add(tag)
    db_session_public.save()

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
    assert session.owner == super_user.username
    assert len(session.players) == 0
    assert len(session.tags) == 1
    assert session.tags[0].name == "tag"
    assert session.tags[0].description == "tag-description"
    assert session.private is False

    db_session_public.players.add(user)
    db_session_public.save()

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
    assert session.owner == super_user.username
    assert len(session.players) == 1
    assert session.players[0] == user.username
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
    foreign_user = django_user_model.objects.create_user(
        is_active=True,
        username="foreigner",
        email="foreigner@example.com",
        password="password!!!",
    )
    staff_user = django_user_model.objects.create_user(
        is_active=True,
        username="staff",
        email="staff@example.com",
        password="password!!!",
    )
    staff_user.is_staff = True
    staff_user.save()

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

    # anonymous users mustn't be able to change it
    client.logout()
    code, response = post_test_url(
        client,
        session.path.replace("<str:session_id>", str(session_object.key)),
        request,
        SuccessResponse,
    )
    assert code == HTTPStatus.UNAUTHORIZED
    assert response.success is False

    (session_object,) = Session.objects.all()
    assert session_object.tags.all()
    assert session_object.description == "session description"

    # non-owning users mustn't be able to change it
    client.force_login(foreign_user)
    code, response = post_test_url(
        client,
        session.path.replace("<str:session_id>", str(session_object.key)),
        request,
        SuccessResponse,
    )
    assert code == HTTPStatus.FORBIDDEN
    assert response.success is False

    (session_object,) = Session.objects.all()
    assert session_object.tags.all()
    assert session_object.description == "session description"

    # owners must be able to change it
    client.force_login(user)
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

    # staff must be able to change it
    request.description = "another description"
    request.tags = [tag2.id]

    client.force_login(staff_user)
    code, response = post_test_url(
        client,
        session.path.replace("<str:session_id>", str(session_object.key)),
        request,
        SuccessResponse,
    )
    assert code == HTTPStatus.OK
    assert response.success

    (session_object,) = Session.objects.all()
    assert session_object.tags.all()
    assert session_object.description == "another description"


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
