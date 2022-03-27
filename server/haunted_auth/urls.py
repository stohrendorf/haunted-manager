from django.urls import path

from hsutils.viewmodels import get_profile, login, logout, regenerate_token, register

from . import views
from .views import confirm_email_token

urlpatterns = [
    login.wrap(views.login),
    logout.wrap(views.logout),
    get_profile.wrap(views.profile),
    register.wrap(views.register),
    regenerate_token.wrap(views.regenerate_token),
    path("email/<str:token>/", confirm_email_token),
]
