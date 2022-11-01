from hsutils.viewmodels import (
    check_session_access,
    create_session,
    delete_session,
    get_sessions,
    get_tags,
)

from . import views

urlpatterns = [
    get_tags.wrap(views.get_tags),
    get_sessions.wrap(views.get_sessions),
    create_session.wrap(views.create_session),
    delete_session.wrap(views.delete_session),
    check_session_access.wrap(views.check_session_access),
]
