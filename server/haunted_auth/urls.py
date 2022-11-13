from django.urls import path

from hsutils.viewmodels import (
    change_email,
    change_password,
    change_username,
    login,
    logout,
    profile,
    regenerate_token,
    register,
)

from . import views
from .views import confirm_email_token

urlpatterns = [
    login.wrap(post_handler=views.login),
    logout.wrap(get_handler=views.logout),
    profile.wrap(get_handler=views.profile),
    register.wrap(post_handler=views.register),
    regenerate_token.wrap(get_handler=views.regenerate_token),
    change_email.wrap(post_handler=views.change_email),
    change_password.wrap(post_handler=views.change_password),
    change_username.wrap(post_handler=views.change_username),
    path("email/<str:token>/", confirm_email_token),
]
