from http import HTTPStatus

import pytest
from django.test import Client

from hsutils.test_utils import get_test_url
from hsutils.viewmodels import AnnouncementsResponse, announcements
from siteapi.models import Announcement


@pytest.mark.django_db
def test_announcements(client: Client, django_user_model):
    assert django_user_model.objects.count() == 0

    def do_test():
        code, response = get_test_url(client, announcements.path, AnnouncementsResponse)
        assert code == HTTPStatus.OK
        assert response is not None
        assert len(response.announcements) == 0

        Announcement.objects.create(message="some message", background_color="dark", text_color="primary")
        code, response = get_test_url(client, announcements.path, AnnouncementsResponse)
        assert code == HTTPStatus.OK
        assert response is not None
        assert len(response.announcements) == 1
        (announcement,) = response.announcements
        assert announcement.message == "some message"
        assert announcement.background_color == "dark"
        assert announcement.text_color == "primary"

    do_test()
    django_user_model.objects.create_user(
        username="user",
        email="user@example.com",
        password="password123",
    )
    Announcement.objects.all().delete()
    do_test()
