from http import HTTPStatus

import pytest
from django.test import Client

from haunted_sessions.models import Tag
from hsutils.test_utils import get_test_url
from hsutils.viewmodels import TagsResponse, tags


@pytest.mark.django_db
def test_tags(client: Client):
    code, response = get_test_url(
        client,
        tags.path,
        TagsResponse,
    )
    assert code == HTTPStatus.OK
    assert response is not None
    assert len(response.tags) == 0

    Tag.objects.create(name="test1", description="description1")

    code, response = get_test_url(
        client,
        tags.path,
        TagsResponse,
    )
    assert code == HTTPStatus.OK
    assert response is not None
    assert len(response.tags) == 1
    assert response.tags[0].name == "test1"
    assert response.tags[0].description == "description1"
