from hsutils.viewmodels import get_announcements, get_server_info

from . import views

urlpatterns = [
    get_announcements.wrap(views.get_announcements),
    get_server_info.wrap(views.get_server_info),
]
