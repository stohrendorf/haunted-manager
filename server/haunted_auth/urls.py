from django.urls import path

from hsutils.viewmodels import (
    change_email,
    change_password,
    get_profile,
    login,
    logout,
    regenerate_token,
    register,
)

from . import views
from .views import confirm_email_token

urlpatterns = [
    login.wrap(views.login),
    logout.wrap(views.logout),
    get_profile.wrap(views.profile),
    register.wrap(views.register),
    regenerate_token.wrap(views.regenerate_token),
    change_email.wrap(views.change_email),
    change_password.wrap(views.change_password),
    path("email/<str:token>/", confirm_email_token),
]
