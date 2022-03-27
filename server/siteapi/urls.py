from hsutils.viewmodels import get_announcements, get_stats

from . import views

urlpatterns = [
    get_announcements.wrap(views.get_announcements),
    get_stats.wrap(views.get_stats),
]
