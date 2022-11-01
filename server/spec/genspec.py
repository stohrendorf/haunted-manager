from pathlib import Path

from endpoints import Endpoint
from generator_django import gen_django
from generator_vue import gen_vue
from structural import ArrayField, BooleanField, Compound, IntegerField, StringField

from spec.endpoints import gather_compounds


class TagName(StringField):
    def __init__(self):
        super().__init__(min_length=1)


class IsoDateTime(StringField):
    def __init__(self):
        super().__init__(regex=r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{6}\+[0-9]{2}:[0-9]{2}")


class StatsResponse(Compound):
    total_users = IntegerField(min=0)
    total_sessions = IntegerField(min=0)


class ProfileInfoResponse(Compound):
    username = StringField(min_length=1)
    authenticated = BooleanField()
    verified = BooleanField()
    email = StringField(nullable=True, min_length=1)
    auth_token = StringField(nullable=True, min_length=1)


class LoginRequest(Compound):
    username = StringField(min_length=1)
    password = StringField(min_length=1)


class RegisterRequest(Compound):
    username = StringField(min_length=1)
    password = StringField(min_length=1)
    email = StringField(min_length=1)


class Tag(Compound):
    id = IntegerField()
    name = StringField(min_length=1)
    description = StringField()


class SessionTag(Compound):
    name = StringField(min_length=1)
    description = StringField(min_length=1)


class TagsResponse(Compound):
    tags = ArrayField(items=Tag())


class SuccessResponse(Compound):
    success = BooleanField()
    message = StringField()


class Session(Compound):
    id = StringField(min_length=1)
    tags = ArrayField(items=SessionTag())
    owner = StringField(min_length=1)
    description = StringField()


class CreateSessionRequest(Compound):
    description = StringField()
    tags = ArrayField(items=IntegerField())


class SessionsResponse(Compound):
    sessions = ArrayField(items=Session())


class DeleteSessionRequest(Compound):
    session_id = StringField(min_length=1)


class Empty(Compound):
    pass


class AnnouncementEntry(Compound):
    message = StringField(min_length=1)
    background_color = StringField(min_length=1)
    text_color = StringField(min_length=1)


class AnnouncementsResponse(Compound):
    announcements = ArrayField(items=AnnouncementEntry())


def write_vue_spec(output: Path, *endpoints: Endpoint):
    all_compounds = gather_compounds(*endpoints)

    vue_spec = gen_vue([x() for x in all_compounds], list(endpoints))
    output.write_text(vue_spec)


def write_django_spec(output: Path, *endpoints: Endpoint):
    all_compounds = gather_compounds(*endpoints)

    django_spec = gen_django([x() for x in all_compounds], list(endpoints))
    output.write_text(django_spec)


endpoints = (
    Endpoint(
        operation_name="getStats",
        path="/api/v0/stats",
        method="get",
        response=StatsResponse(),
    ),
    Endpoint(
        operation_name="getTags",
        path="/api/v0/tags",
        method="get",
        response=TagsResponse(),
    ),
    Endpoint(
        operation_name="getSessions",
        path="/api/v0/sessions",
        method="get",
        response=SessionsResponse(),
    ),
    Endpoint(
        operation_name="createSession",
        path="/api/v0/sessions/create",
        method="post",
        response=SuccessResponse(),
        body=CreateSessionRequest(),
    ),
    Endpoint(
        operation_name="deleteSession",
        path="/api/v0/sessions/delete",
        method="post",
        response=SuccessResponse(),
        body=DeleteSessionRequest(),
    ),
    Endpoint(
        operation_name="getAnnouncements",
        path="/api/v0/announcements",
        method="get",
        response=AnnouncementsResponse(),
    ),
    Endpoint(
        operation_name="getProfile",
        path="/api/v0/auth/profile",
        method="get",
        response=ProfileInfoResponse(),
    ),
    Endpoint(
        operation_name="regenerateToken",
        path="/api/v0/auth/regenerate-token",
        method="get",
        response=Empty(),
    ),
    Endpoint(
        operation_name="login",
        path="/api/v0/auth/login",
        method="post",
        response=SuccessResponse(),
        body=LoginRequest(),
    ),
    Endpoint(
        operation_name="register",
        path="/api/v0/auth/register",
        method="post",
        response=SuccessResponse(),
        body=RegisterRequest(),
    ),
    Endpoint(
        operation_name="logout",
        path="/api/v0/auth/logout",
        method="get",
        response=Empty(),
    ),
)

write_vue_spec(
    Path(__file__).parent.parent.parent / "frontend" / "src" / "components" / "ApiService.ts",
    *endpoints,
)

write_django_spec(
    Path(__file__).parent.parent / "hsutils" / "viewmodels.py",
    *endpoints,
)
