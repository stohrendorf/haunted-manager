from pathlib import Path

from endpoints import Endpoint, HttpMethod, gather_compounds
from generator_django import gen_django
from generator_vue import gen_vue
from structural import ArrayField, BooleanField, Compound, IntegerField, StringField


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


class ChangeUsernameRequest(Compound):
    username = StringField(min_length=1)


class LoginRequest(Compound):
    username = StringField(min_length=1)
    password = StringField(min_length=1)


class RegisterRequest(Compound):
    username = StringField(min_length=1)
    password = StringField(min_length=1)
    email = StringField(min_length=1)


class ChangePasswordRequest(Compound):
    password = StringField(min_length=1)


class ChangeEmailRequest(Compound):
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
    players = ArrayField(items=StringField(min_length=1))


class CreateSessionRequest(Compound):
    description = StringField()
    tags = ArrayField(items=IntegerField())


class SessionsResponse(Compound):
    sessions = ArrayField(items=Session())


class DeleteSessionRequest(Compound):
    session_id = StringField(min_length=1)


class SessionAccessRequest(Compound):
    username = StringField(min_length=1)
    auth_token = StringField(min_length=1)
    session_id = StringField(min_length=1)
    api_key = StringField(min_length=1)


class SessionPlayers(Compound):
    session_id = StringField(min_length=1)
    usernames = ArrayField(items=StringField(min_length=1))


class SessionsPlayersRequest(Compound):
    sessions = ArrayField(items=SessionPlayers())
    api_key = StringField(min_length=1)


class Empty(Compound):
    pass


class AnnouncementEntry(Compound):
    message = StringField(min_length=1)
    background_color = StringField(min_length=1)
    text_color = StringField(min_length=1)


class AnnouncementsResponse(Compound):
    announcements = ArrayField(items=AnnouncementEntry())


def write_vue_spec(output: Path, endpoints: dict[str, dict[HttpMethod, Endpoint]]):
    all_compounds = gather_compounds(endpoints)

    vue_spec = gen_vue([x() for x in all_compounds], endpoints)
    output.write_text(vue_spec)


def write_django_spec(output: Path, endpoints: dict[str, dict[HttpMethod, Endpoint]]):
    all_compounds = gather_compounds(endpoints)

    django_spec = gen_django([x() for x in all_compounds], endpoints)
    output.write_text(django_spec)


def main():
    endpoints = {
        "/api/v0/stats": {
            HttpMethod.GET: Endpoint(
                operation_name="getStats",
                response=StatsResponse(),
            )
        },
        "/api/v0/tags": {
            HttpMethod.GET: Endpoint(
                operation_name="getTags",
                response=TagsResponse(),
            )
        },
        "/api/v0/sessions": {
            HttpMethod.GET: Endpoint(
                operation_name="getSessions",
                response=SessionsResponse(),
            )
        },
        "/api/v0/sessions/create": {
            HttpMethod.POST: Endpoint(
                operation_name="createSession",
                response=SuccessResponse(),
                body=CreateSessionRequest(),
            )
        },
        "/api/v0/sessions/delete": {
            HttpMethod.POST: Endpoint(
                operation_name="deleteSession",
                response=SuccessResponse(),
                body=DeleteSessionRequest(),
            )
        },
        "/api/v0/sessions/check-access": {
            HttpMethod.POST: Endpoint(
                operation_name="checkSessionAccess",
                response=SuccessResponse(),
                body=SessionAccessRequest(),
            )
        },
        "/api/v0/sessions/session-players": {
            HttpMethod.POST: Endpoint(
                operation_name="updateSessionsPlayers",
                response=Empty(),
                body=SessionsPlayersRequest(),
            )
        },
        "/api/v0/announcements": {
            HttpMethod.GET: Endpoint(
                operation_name="getAnnouncements",
                response=AnnouncementsResponse(),
            )
        },
        "/api/v0/auth/profile": {
            HttpMethod.GET: Endpoint(
                operation_name="getProfile",
                response=ProfileInfoResponse(),
            )
        },
        "/api/v0/auth/change-username": {
            HttpMethod.POST: Endpoint(
                operation_name="changeUsername",
                response=SuccessResponse(),
                body=ChangeUsernameRequest(),
            )
        },
        "/api/v0/auth/regenerate-token": {
            HttpMethod.GET: Endpoint(
                operation_name="regenerateToken",
                response=Empty(),
            )
        },
        "/api/v0/auth/login": {
            HttpMethod.POST: Endpoint(
                operation_name="login",
                response=SuccessResponse(),
                body=LoginRequest(),
            )
        },
        "/api/v0/auth/register": {
            HttpMethod.POST: Endpoint(
                operation_name="register",
                response=SuccessResponse(),
                body=RegisterRequest(),
            )
        },
        "/api/v0/auth/change-password": {
            HttpMethod.POST: Endpoint(
                operation_name="changePassword",
                response=SuccessResponse(),
                body=ChangePasswordRequest(),
            )
        },
        "/api/v0/auth/change-email": {
            HttpMethod.POST: Endpoint(
                operation_name="changeEmail",
                response=SuccessResponse(),
                body=ChangeEmailRequest(),
            )
        },
        "/api/v0/auth/logout": {
            HttpMethod.GET: Endpoint(
                operation_name="logout",
                response=Empty(),
            )
        },
    }

    write_vue_spec(
        Path(__file__).parent.parent.parent / "frontend" / "src" / "components" / "ApiService.ts",
        endpoints,
    )

    write_django_spec(
        Path(__file__).parent.parent / "hsutils" / "viewmodels.py",
        endpoints,
    )


if __name__ == "__main__":
    main()
