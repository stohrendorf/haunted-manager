from hsutils.viewmodels import create_session, delete_session, get_sessions, get_tags

from . import views

urlpatterns = [
    get_tags.wrap(views.get_tags),
    get_sessions.wrap(views.get_sessions),
    create_session.wrap(views.create_session),
    delete_session.wrap(views.delete_session),
]
