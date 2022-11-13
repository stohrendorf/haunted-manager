from hsutils.viewmodels import announcements, server_info

from . import views

urlpatterns = [
    announcements.wrap(get_handler=views.get_announcements),
    server_info.wrap(get_handler=views.get_server_info),
]
