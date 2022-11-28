from hsutils.viewmodels import download_ghost as download_ghost_endpoint
from hsutils.viewmodels import ghosts, quota, single_ghost, staging_ghosts

from .views import (
    delete_single_ghost,
    download_ghost,
    get_published_ghosts,
    get_quota,
    get_single_ghost,
    get_staging_ghosts,
    update_single_ghost,
    upload,
)

urlpatterns = [
    ghosts.wrap(get_handler=get_published_ghosts, post_handler=upload),
    quota.wrap(get_handler=get_quota),
    staging_ghosts.wrap(get_handler=get_staging_ghosts),
    single_ghost.wrap(
        get_handler=get_single_ghost,
        post_handler=update_single_ghost,
        delete_handler=delete_single_ghost,
    ),
    download_ghost_endpoint.wrap(get_handler=download_ghost),
]
