from pathlib import Path

from endpoints import ApiPath, Endpoint, HttpMethod, gather_compounds
from generator_django import gen_django
from generator_vue import gen_vue
from structural import ArrayField, BooleanField, Compound, IntegerField, StringField

from spec.openapi import gen_openapi


class TagName(StringField):
    def __init__(self):
        super().__init__(min_length=1)


class IsoDateTime(StringField):
    def __init__(self):
        # 2022-11-20T13:45:18.188Z
        super().__init__(regex=r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]+(\+[0-9]{2}:[0-9]{2}|Z)")


class TimeSpan(Compound):
    start = IsoDateTime()
    end = IsoDateTime()


class ServerInfoResponse(Compound):
    total_users = IntegerField(min=0)
    total_sessions = IntegerField(min=0)
    coop_url = StringField(min_length=1)


class ProfileInfoResponse(Compound):
    username = StringField(min_length=1)
    authenticated = BooleanField()
    verified = BooleanField()
    email = StringField(nullable=True, min_length=1)
    auth_token = StringField(nullable=True, min_length=1)
    is_staff = BooleanField()


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
    time = TimeSpan(nullable=True)


class CreateSessionRequest(Compound):
    description = StringField()
    tags = ArrayField(items=IntegerField())
    time = TimeSpan(nullable=True)


class SessionsResponse(Compound):
    sessions = ArrayField(items=Session())


class SessionResponse(Compound):
    session = Session(nullable=True)


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


def write_vue_spec(output: Path, endpoints: dict[ApiPath, dict[HttpMethod, Endpoint]]):
    all_compounds = gather_compounds(endpoints)

    vue_spec = gen_vue([x() for x in all_compounds], endpoints)
    output.write_text(vue_spec)


def write_django_spec(output: Path, endpoints: dict[ApiPath, dict[HttpMethod, Endpoint]]):
    all_compounds = gather_compounds(endpoints)

    django_spec = gen_django([x() for x in all_compounds], endpoints)
    output.write_text(django_spec)


def write_openapi_spec(output: Path, endpoints: dict[ApiPath, dict[HttpMethod, Endpoint]]):
    all_compounds = gather_compounds(endpoints)

    openapi_spec = gen_openapi([x() for x in all_compounds], endpoints)
    output.write_text(openapi_spec)


def main():
    endpoints = {
        ApiPath("/api/v0/server-info", "serverInfo"): {
            HttpMethod.GET: Endpoint(
                operation_name="getServerInfo",
                response=ServerInfoResponse(),
            ),
        },
        ApiPath("/api/v0/tags", "tags"): {
            HttpMethod.GET: Endpoint(
                operation_name="getTags",
                response=TagsResponse(),
            ),
        },
        ApiPath("/api/v0/sessions", "sessions"): {
            HttpMethod.GET: Endpoint(
                operation_name="getSessions",
                response=SessionsResponse(),
            ),
            HttpMethod.POST: Endpoint(
                operation_name="createSession",
                response=SuccessResponse(),
                body=CreateSessionRequest(),
            ),
        },
        ApiPath("/api/v0/sessions/<str:sessionId>", "session"): {
            HttpMethod.GET: Endpoint(
                operation_name="getSession",
                response=SessionResponse(),
            ),
            HttpMethod.POST: Endpoint(
                operation_name="editSession",
                response=SuccessResponse(),
                body=CreateSessionRequest(),
            ),
            HttpMethod.DELETE: Endpoint(
                operation_name="deleteSession",
                response=SuccessResponse(),
            ),
        },
        ApiPath("/api/v0/sessions/check-access", "sessionAccess"): {
            HttpMethod.POST: Endpoint(
                operation_name="checkSessionAccess",
                response=SuccessResponse(),
                body=SessionAccessRequest(),
            ),
        },
        ApiPath("/api/v0/sessions/session-players", "sessionPlayers"): {
            HttpMethod.POST: Endpoint(
                operation_name="updateSessionsPlayers",
                response=Empty(),
                body=SessionsPlayersRequest(),
            ),
        },
        ApiPath("/api/v0/announcements", "announcements"): {
            HttpMethod.GET: Endpoint(
                operation_name="getAnnouncements",
                response=AnnouncementsResponse(),
            ),
        },
        ApiPath("/api/v0/auth/profile", "profile"): {
            HttpMethod.GET: Endpoint(
                operation_name="getProfile",
                response=ProfileInfoResponse(),
            ),
        },
        ApiPath("/api/v0/auth/change-username", "changeUsername"): {
            HttpMethod.POST: Endpoint(
                operation_name="changeUsername",
                response=SuccessResponse(),
                body=ChangeUsernameRequest(),
            ),
        },
        ApiPath("/api/v0/auth/regenerate-token", "regenerateToken"): {
            HttpMethod.GET: Endpoint(
                operation_name="regenerateToken",
                response=Empty(),
            ),
        },
        ApiPath("/api/v0/auth/login", "login"): {
            HttpMethod.POST: Endpoint(
                operation_name="login",
                response=SuccessResponse(),
                body=LoginRequest(),
            ),
        },
        ApiPath("/api/v0/auth/register", "register"): {
            HttpMethod.POST: Endpoint(
                operation_name="register",
                response=SuccessResponse(),
                body=RegisterRequest(),
            ),
        },
        ApiPath("/api/v0/auth/change-password", "changePassword"): {
            HttpMethod.POST: Endpoint(
                operation_name="changePassword",
                response=SuccessResponse(),
                body=ChangePasswordRequest(),
            ),
        },
        ApiPath("/api/v0/auth/change-email", "changeEmail"): {
            HttpMethod.POST: Endpoint(
                operation_name="changeEmail",
                response=SuccessResponse(),
                body=ChangeEmailRequest(),
            ),
        },
        ApiPath("/api/v0/auth/logout", "logout"): {
            HttpMethod.GET: Endpoint(
                operation_name="logout",
                response=Empty(),
            ),
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

    write_openapi_spec(
        Path(__file__).parent.parent / "hsutils" / "openapi.json",
        endpoints,
    )


if __name__ == "__main__":
    main()
