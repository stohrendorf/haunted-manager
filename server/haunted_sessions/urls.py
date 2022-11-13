from hsutils.viewmodels import session, session_access, session_players, sessions, tags

from . import views

urlpatterns = [
    tags.wrap(get_handler=views.get_tags),
    sessions.wrap(get_handler=views.get_sessions, post_handler=views.create_session),
    session.wrap(get_handler=views.get_session, post_handler=views.edit_session, delete_handler=views.delete_session),
    session_access.wrap(post_handler=views.check_session_access),
    session_players.wrap(post_handler=views.update_sessions_players),
]
