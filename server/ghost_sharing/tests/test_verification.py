from http import HTTPStatus
from pathlib import Path

from ghost_sharing.views import _verify_ghost_data_extension
from hsutils.schemas.SuccessResponse import SuccessResponse


def test_verify_ghost_data_extension():
    assert _verify_ghost_data_extension(Path("foo.yml")) is None
    assert _verify_ghost_data_extension(Path("foo.bin")) is None
    status, response = _verify_ghost_data_extension(Path("foo.yaml"))
    assert status == HTTPStatus.BAD_REQUEST
    assert isinstance(response, SuccessResponse)
    assert response.success is False
    assert "foo.yaml" in response.message
