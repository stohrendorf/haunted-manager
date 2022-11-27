from io import SEEK_END
from typing import IO, Iterable

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from minio import Minio, S3Error
from minio.commonconfig import ENABLED, CopySource, Filter
from minio.lifecycleconfig import Expiration, LifecycleConfig, Rule

from ghost_sharing.models import Ghost


def _create_client() -> Minio:
    return Minio(
        endpoint=settings.MINIO_URL,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_SECURE,
    )


def prepare_buckets():
    client = _create_client()
    if not client.bucket_exists(settings.MINIO_GHOST_BUCKET_STAGING):
        client.make_bucket(settings.MINIO_GHOST_BUCKET_STAGING)
        client.set_bucket_lifecycle(
            settings.MINIO_GHOST_BUCKET_STAGING,
            LifecycleConfig(
                [
                    Rule(
                        ENABLED,
                        expiration=Expiration(days=1),
                        rule_filter=Filter(prefix=""),
                    ),
                ],
            ),
        )
    if not client.bucket_exists(settings.MINIO_GHOST_BUCKET):
        client.make_bucket(settings.MINIO_GHOST_BUCKET)


def _list_ghosts(user: AbstractUser, bucket: str) -> Iterable[tuple[str, int]]:
    client = _create_client()
    return (
        (ob.object_name, ob.size)
        for ob in client.list_objects(
            bucket,
            prefix=f"{user.id}/",
            recursive=True,
        )
        if not ob.is_dir
    )


def _object_name_of(ghost: Ghost) -> str:
    return f"{ghost.owner.id}/{ghost.file_id.hex}/{ghost.original_filename}"


def ghost_data_exists(ghost: Ghost) -> bool:
    client = _create_client()
    try:
        client.stat_object(
            settings.MINIO_GHOST_BUCKET if ghost.published else settings.MINIO_GHOST_BUCKET_STAGING,
            object_name=_object_name_of(ghost),
        )
        return True
    except S3Error as e:
        if e.code == "NoSuchKey":
            return False
        raise


def get_ghost_data(ghost: Ghost) -> bytes:
    client = _create_client()
    with client.get_object(
        settings.MINIO_GHOST_BUCKET if ghost.published else settings.MINIO_GHOST_BUCKET_STAGING,
        object_name=_object_name_of(ghost),
    ) as response:
        return response.read()


def get_staging_ghosts(user: AbstractUser) -> Iterable[tuple[str, int]]:
    return _list_ghosts(user, settings.MINIO_GHOST_BUCKET_STAGING)


def get_published_ghosts(user: AbstractUser) -> Iterable[tuple[str, int]]:
    return _list_ghosts(user, settings.MINIO_GHOST_BUCKET)


def get_user_ghost_total_size(user: AbstractUser) -> int:
    return sum(size for _, size in get_staging_ghosts(user)) + sum(size for _, size in get_published_ghosts(user))


def put_staging_ghost(ghost: Ghost, data: IO):
    data.seek(0, SEEK_END)
    length = data.tell()
    data.seek(0)
    client = _create_client()
    client.put_object(
        settings.MINIO_GHOST_BUCKET_STAGING,
        object_name=_object_name_of(ghost),
        data=data,
        length=length,
    )


def _move_ghost(ghost: Ghost, src_bucket: str, dst_bucket: str):
    client = _create_client()
    object_name = f"{ghost.owner.id}/{ghost.file_id.hex}/{ghost.original_filename}"
    client.copy_object(
        dst_bucket,
        object_name,
        CopySource(
            src_bucket,
            object_name,
        ),
    )
    client.remove_object(
        src_bucket,
        object_name,
    )


def publish_ghost(ghost: Ghost):
    _move_ghost(ghost, settings.MINIO_GHOST_BUCKET_STAGING, settings.MINIO_GHOST_BUCKET)
    ghost.published = True


def unpublish_ghost(ghost: Ghost):
    _move_ghost(ghost, settings.MINIO_GHOST_BUCKET, settings.MINIO_GHOST_BUCKET_STAGING)
    ghost.published = False
