import hashlib
import logging
import tarfile
import uuid
from datetime import timedelta
from http import HTTPStatus
from io import BytesIO
from pathlib import Path

import yaml
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db.models import Sum
from django.db.transaction import atomic
from django.http import FileResponse, HttpRequest

from hsutils.auth import require_authenticated
from hsutils.minio import (
    delete_ghost,
    get_ghost_data,
    ghost_data_exists,
    publish_ghost,
    put_staging_ghost,
    unpublish_ghost,
)
from hsutils.viewmodels import (
    GhostFileResponse,
    GhostFileResponseEntry,
    GhostFilesResponse,
    GhostInfoRequest,
    LevelInfo,
    LevelsResponse,
    QuotaResponse,
    SuccessResponse,
    Tag,
)

from .models import Gameflow, Ghost, GhostFinishType, Level
from .models import Tag as TagModel


class SafeLoaderIgnoreUnknown(yaml.SafeLoader):
    def ignore_unknown(self, node):
        if isinstance(node, yaml.ScalarNode):
            return node.value
        return None


SafeLoaderIgnoreUnknown.add_constructor(None, SafeLoaderIgnoreUnknown.ignore_unknown)


def _remove_expired_staging_ghosts(request: HttpRequest):
    for ghost in Ghost.objects.filter(published=False, owner=request.user).all():
        if not ghost_data_exists(ghost):
            ghost.delete()


@require_authenticated(response=QuotaResponse(max=0, current=0))
def get_quota(request: HttpRequest) -> QuotaResponse:
    return QuotaResponse(
        max=settings.GHOST_QUOTA,
        current=Ghost.objects.filter(owner=request.user).all().aggregate(Sum("data_size"))["data_size__sum"] or 0,
    )


@require_authenticated(response=SuccessResponse(success=False, message="not authorized"))
@atomic
def upload(request: HttpRequest, files: dict[str, UploadedFile]) -> SuccessResponse | tuple[int, SuccessResponse]:
    for filename, data in files.items():
        if not filename.endswith(".tar.xz"):
            return HTTPStatus.BAD_REQUEST, SuccessResponse(success=False, message="Invalid file format")
        elif data.size > settings.MAX_GHOST_SIZE:
            return HTTPStatus.BAD_REQUEST, SuccessResponse(success=False, message="File too large")
        elif (
            data.size
            + (Ghost.objects.filter(owner=request.user).all().aggregate(Sum("data_size"))["data_size__sum"] or 0)
            > settings.GHOST_QUOTA
        ):
            return HTTPStatus.BAD_REQUEST, SuccessResponse(success=False, message="Quota exceeded")

        with BytesIO() as tmp_file:
            try:
                file_hash = hashlib.md5()
                for chunk in data.chunks():
                    file_hash.update(chunk)
                    tmp_file.write(chunk)
                data_hash = file_hash.hexdigest()
            except Exception:
                logging.fatal("File save failed", exc_info=True)
                raise

            tmp_file.seek(0)

            try:
                with tarfile.open(fileobj=tmp_file) as archive:
                    for archive_member in archive.getmembers():
                        if Path(archive_member.name).suffix not in (".yml", ".bin"):
                            return HTTPStatus.BAD_REQUEST, SuccessResponse(
                                success=False,
                                message=f"invalid filename {archive_member.name}",
                            )
                        if not archive_member.isfile():
                            return HTTPStatus.BAD_REQUEST, SuccessResponse(
                                success=False,
                                message=f"not a file: {archive_member.name}",
                            )
                        if Path(archive_member.name).suffix == ".yml":
                            with archive.extractfile(archive_member) as extracted:
                                yml_data = yaml.load(extracted, Loader=SafeLoaderIgnoreUnknown)
                            unknown_gameflow, _ = Gameflow.objects.get_or_create(
                                identifier="unknown",
                                title="unknown",
                            )
                            try:
                                level = Level.objects.get(
                                    gameflow=unknown_gameflow,
                                    identifier=yml_data["ghost"]["level"],
                                )
                            except Level.DoesNotExist:
                                level = Level.objects.create(
                                    gameflow=unknown_gameflow,
                                    identifier=yml_data["ghost"]["level"],
                                    title=yml_data["ghost"]["level"],
                                )

                            staging_ghost = Ghost.objects.create(
                                owner=request.user,
                                file_id=uuid.uuid4(),
                                level=level,
                                duration=timedelta(seconds=int(yml_data["ghost"]["duration"]) / 30),
                                hash=data_hash,
                                original_filename=filename,
                                published=False,
                                finish_type=yml_data["ghost"]["finishState"],
                                data_size=data.size,
                            )
                            staging_ghost.save()
                put_staging_ghost(staging_ghost, tmp_file)
            except Exception:
                logging.fatal("File save failed", exc_info=True)
                raise

    return SuccessResponse(success=True, message="")


def _ghost_to_response(ghost: Ghost) -> GhostFileResponseEntry:
    return GhostFileResponseEntry(
        username=ghost.owner.username,
        description=ghost.description,
        id=ghost.id,
        tags=[
            Tag(
                description=tag.description,
                id=tag.id,
                name=tag.name,
            )
            for tag in ghost.tags.all()
        ],
        level_display=f"{ghost.level.gameflow.title} - {ghost.level.title}",
        level_identifier=ghost.level.identifier,
        level_id=ghost.level.id,
        duration=int(ghost.duration.total_seconds()),
        size=ghost.data_size,
        finish_type=GhostFinishType(ghost.finish_type).value,
        downloads=ghost.downloads,
        published=ghost.published,
    )


def _get_ghosts(published: bool) -> GhostFilesResponse:
    return GhostFilesResponse(
        files=[_ghost_to_response(ghost) for ghost in Ghost.objects.filter(published=published).all()],
    )


def get_published_ghosts(request: HttpRequest) -> GhostFilesResponse:
    return _get_ghosts(True)


@atomic
def get_staging_ghosts(request: HttpRequest) -> GhostFilesResponse:
    _remove_expired_staging_ghosts(request)
    return _get_ghosts(False)


@require_authenticated(response=SuccessResponse(success=False, message="not allowed"))
def delete_single_ghost(request: HttpRequest, id: int) -> SuccessResponse | tuple[int, SuccessResponse]:
    try:
        ghost: Ghost = Ghost.objects.get(id=id)
    except Ghost.DoesNotExist:
        return HTTPStatus.NOT_FOUND, SuccessResponse(success=False, message="ghost not found")

    if request.user.is_staff or request.user.is_superuser:
        pass
    elif request.user != ghost.owner:
        return HTTPStatus.FORBIDDEN, SuccessResponse(
            message="not allowed to edit this session",
            success=False,
        )

    delete_ghost(ghost)
    ghost.delete()
    return SuccessResponse(success=True, message="")


@require_authenticated(response=SuccessResponse(success=False, message="not allowed"))
def update_single_ghost(
    request: HttpRequest,
    id: int,
    body: GhostInfoRequest,
) -> SuccessResponse | tuple[int, SuccessResponse]:
    try:
        ghost: Ghost = Ghost.objects.get(id=id)
    except Ghost.DoesNotExist:
        return HTTPStatus.NOT_FOUND, SuccessResponse(success=False, message="ghost not found")

    if request.user.is_staff or request.user.is_superuser:
        pass
    elif request.user != ghost.owner:
        return HTTPStatus.FORBIDDEN, SuccessResponse(
            message="not allowed to edit this session",
            success=False,
        )

    if ghost.published != body.published:
        if body.published:
            publish_ghost(ghost)
        else:
            unpublish_ghost(ghost)
    ghost.description = body.description
    ghost.tags.set(TagModel.objects.filter(id__in=body.tags).all())
    ghost.level = Level.objects.get(id=body.level_id)
    ghost.save()
    return SuccessResponse(success=True, message="")


@require_authenticated(response=SuccessResponse(success=False, message="not allowed"))
@atomic
def download_ghost(request: HttpRequest, id: int) -> FileResponse:
    try:
        ghost: Ghost = Ghost.objects.get(id=id)
    except Ghost.DoesNotExist:
        return FileResponse(status=HTTPStatus.NOT_FOUND)

    if not ghost_data_exists(ghost):
        ghost.delete()
        return FileResponse(status=HTTPStatus.NOT_FOUND)

    ghost.downloads += 1
    ghost.save()

    return FileResponse(
        BytesIO(get_ghost_data(ghost)),
        filename=ghost.original_filename,
        as_attachment=True,
    )


def get_single_ghost(request: HttpRequest, id: int) -> GhostFileResponse | tuple[int, GhostFileResponse]:
    try:
        ghost = Ghost.objects.get(id=id)
    except Ghost.DoesNotExist:
        return HTTPStatus.NOT_FOUND, GhostFileResponse(ghost=None)
    return GhostFileResponse(ghost=_ghost_to_response(ghost))


def get_alternative_levels(request: HttpRequest, identifier: str) -> LevelsResponse:
    return LevelsResponse(
        levels=[
            LevelInfo(
                id=level.id,
                identifier=level.identifier,
                title=f"{level.gameflow.title} - {level.title}",
            )
            for level in Level.objects.filter(identifier=identifier).all()
        ]
    )
