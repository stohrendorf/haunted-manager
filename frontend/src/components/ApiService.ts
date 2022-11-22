/* eslint-disable no-empty */
// noinspection RedundantIfStatementJS
export interface IAnnouncementEntry {
  background_color: string;
  message: string;
  text_color: string;
}
export interface IAnnouncementsResponse {
  announcements: IAnnouncementEntry[];
}
export interface IChangeEmailRequest {
  email: string;
}
export interface IChangePasswordRequest {
  password: string;
}
export interface IChangeUsernameRequest {
  username: string;
}
export interface ICreateSessionRequest {
  description: string;
  tags: number[];
  time: ITimeSpan | null;
}
export interface IEmpty {}
export interface ILoginRequest {
  password: string;
  username: string;
}
export interface IProfileInfoResponse {
  auth_token: string | null;
  authenticated: boolean;
  email: string | null;
  is_staff: boolean;
  username: string;
  verified: boolean;
}
export interface IRegisterRequest {
  email: string;
  password: string;
  username: string;
}
export interface IServerInfoResponse {
  coop_url: string;
  total_sessions: number;
  total_users: number;
}
export interface ISession {
  description: string;
  id: string;
  owner: string;
  players: string[];
  tags: ISessionTag[];
  time: ITimeSpan | null;
}
export interface ISessionAccessRequest {
  api_key: string;
  auth_token: string;
  session_id: string;
  username: string;
}
export interface ISessionPlayers {
  session_id: string;
  usernames: string[];
}
export interface ISessionResponse {
  session: ISession | null;
}
export interface ISessionTag {
  description: string;
  name: string;
}
export interface ISessionsPlayersRequest {
  api_key: string;
  sessions: ISessionPlayers[];
}
export interface ISessionsResponse {
  sessions: ISession[];
}
export interface ISuccessResponse {
  message: string;
  success: boolean;
}
export interface ITag {
  description: string;
  id: number;
  name: string;
}
export interface ITagsResponse {
  tags: ITag[];
}
export interface ITimeSpan {
  end: string;
  start: string;
}
function validateAnnouncementEntry(data: IAnnouncementEntry): void {
  if (data.background_color === undefined)
    throw new SchemaValidationError(
      "AnnouncementEntry.background_color is undefined"
    );
  if (data.background_color === null)
    throw new SchemaValidationError(
      "AnnouncementEntry.background_color is null"
    );
  if (data.background_color.length < 1)
    throw new SchemaValidationError(
      "AnnouncementEntry.background_color is too short"
    );
  if (data.message === undefined)
    throw new SchemaValidationError("AnnouncementEntry.message is undefined");
  if (data.message === null)
    throw new SchemaValidationError("AnnouncementEntry.message is null");
  if (data.message.length < 1)
    throw new SchemaValidationError("AnnouncementEntry.message is too short");
  if (data.text_color === undefined)
    throw new SchemaValidationError(
      "AnnouncementEntry.text_color is undefined"
    );
  if (data.text_color === null)
    throw new SchemaValidationError("AnnouncementEntry.text_color is null");
  if (data.text_color.length < 1)
    throw new SchemaValidationError(
      "AnnouncementEntry.text_color is too short"
    );
}
function validateAnnouncementsResponse(data: IAnnouncementsResponse): void {
  if (data.announcements === undefined)
    throw new SchemaValidationError(
      "AnnouncementsResponse.announcements is undefined"
    );
  if (data.announcements === null)
    throw new SchemaValidationError(
      "AnnouncementsResponse.announcements is null"
    );
  for (const fieldData of data.announcements) {
    validateAnnouncementEntry(fieldData);
  }
}
function validateChangeEmailRequest(data: IChangeEmailRequest): void {
  if (data.email === undefined)
    throw new SchemaValidationError("ChangeEmailRequest.email is undefined");
  if (data.email === null)
    throw new SchemaValidationError("ChangeEmailRequest.email is null");
  if (data.email.length < 1)
    throw new SchemaValidationError("ChangeEmailRequest.email is too short");
}
function validateChangePasswordRequest(data: IChangePasswordRequest): void {
  if (data.password === undefined)
    throw new SchemaValidationError(
      "ChangePasswordRequest.password is undefined"
    );
  if (data.password === null)
    throw new SchemaValidationError("ChangePasswordRequest.password is null");
  if (data.password.length < 1)
    throw new SchemaValidationError(
      "ChangePasswordRequest.password is too short"
    );
}
function validateChangeUsernameRequest(data: IChangeUsernameRequest): void {
  if (data.username === undefined)
    throw new SchemaValidationError(
      "ChangeUsernameRequest.username is undefined"
    );
  if (data.username === null)
    throw new SchemaValidationError("ChangeUsernameRequest.username is null");
  if (data.username.length < 1)
    throw new SchemaValidationError(
      "ChangeUsernameRequest.username is too short"
    );
}
function validateCreateSessionRequest(data: ICreateSessionRequest): void {
  if (data.description === undefined)
    throw new SchemaValidationError(
      "CreateSessionRequest.description is undefined"
    );
  if (data.description === null)
    throw new SchemaValidationError("CreateSessionRequest.description is null");
  if (data.description.length > 512)
    throw new SchemaValidationError(
      "CreateSessionRequest.description is too long"
    );
  if (data.tags === undefined)
    throw new SchemaValidationError("CreateSessionRequest.tags is undefined");
  if (data.tags === null)
    throw new SchemaValidationError("CreateSessionRequest.tags is null");
  for (const fieldData of data.tags) {
    if (fieldData === undefined)
      throw new SchemaValidationError("CreateSessionRequest.tags is undefined");
    if (fieldData === null)
      throw new SchemaValidationError("CreateSessionRequest.tags is null");
  }

  if (data.time === undefined)
    throw new SchemaValidationError("CreateSessionRequest.time is undefined");
  if (data.time !== null) {
    validateTimeSpan(data.time);
  }
}
function validateEmpty(data: IEmpty): void {}
function validateIsoDateTime(data?: string | null): void {
  if (data === undefined)
    throw new SchemaValidationError("IsoDateTime is undefined");
  if (data === null) throw new SchemaValidationError("IsoDateTime is null");
  if (
    !data.match(
      /^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]+(\+[0-9]{2}:[0-9]{2}|Z)$/
    )
  )
    throw new SchemaValidationError("IsoDateTime has an invalid format");
}
function validateLoginRequest(data: ILoginRequest): void {
  if (data.password === undefined)
    throw new SchemaValidationError("LoginRequest.password is undefined");
  if (data.password === null)
    throw new SchemaValidationError("LoginRequest.password is null");
  if (data.password.length < 1)
    throw new SchemaValidationError("LoginRequest.password is too short");
  if (data.username === undefined)
    throw new SchemaValidationError("LoginRequest.username is undefined");
  if (data.username === null)
    throw new SchemaValidationError("LoginRequest.username is null");
  if (data.username.length < 1)
    throw new SchemaValidationError("LoginRequest.username is too short");
}
function validateProfileInfoResponse(data: IProfileInfoResponse): void {
  if (data.auth_token === undefined)
    throw new SchemaValidationError(
      "ProfileInfoResponse.auth_token is undefined"
    );
  if (data.auth_token !== null) {
    if (data.auth_token.length < 1)
      throw new SchemaValidationError(
        "ProfileInfoResponse.auth_token is too short"
      );
  }
  if (data.authenticated === undefined)
    throw new SchemaValidationError(
      "ProfileInfoResponse.authenticated is undefined"
    );
  if (data.authenticated === null)
    throw new SchemaValidationError(
      "ProfileInfoResponse.authenticated is null"
    );
  if (data.email === undefined)
    throw new SchemaValidationError("ProfileInfoResponse.email is undefined");
  if (data.email !== null) {
    if (data.email.length < 1)
      throw new SchemaValidationError("ProfileInfoResponse.email is too short");
  }
  if (data.is_staff === undefined)
    throw new SchemaValidationError(
      "ProfileInfoResponse.is_staff is undefined"
    );
  if (data.is_staff === null)
    throw new SchemaValidationError("ProfileInfoResponse.is_staff is null");
  if (data.username === undefined)
    throw new SchemaValidationError(
      "ProfileInfoResponse.username is undefined"
    );
  if (data.username === null)
    throw new SchemaValidationError("ProfileInfoResponse.username is null");
  if (data.username.length < 1)
    throw new SchemaValidationError(
      "ProfileInfoResponse.username is too short"
    );
  if (data.verified === undefined)
    throw new SchemaValidationError(
      "ProfileInfoResponse.verified is undefined"
    );
  if (data.verified === null)
    throw new SchemaValidationError("ProfileInfoResponse.verified is null");
}
function validateRegisterRequest(data: IRegisterRequest): void {
  if (data.email === undefined)
    throw new SchemaValidationError("RegisterRequest.email is undefined");
  if (data.email === null)
    throw new SchemaValidationError("RegisterRequest.email is null");
  if (data.email.length < 1)
    throw new SchemaValidationError("RegisterRequest.email is too short");
  if (data.password === undefined)
    throw new SchemaValidationError("RegisterRequest.password is undefined");
  if (data.password === null)
    throw new SchemaValidationError("RegisterRequest.password is null");
  if (data.password.length < 1)
    throw new SchemaValidationError("RegisterRequest.password is too short");
  if (data.username === undefined)
    throw new SchemaValidationError("RegisterRequest.username is undefined");
  if (data.username === null)
    throw new SchemaValidationError("RegisterRequest.username is null");
  if (data.username.length < 1)
    throw new SchemaValidationError("RegisterRequest.username is too short");
}
function validateServerInfoResponse(data: IServerInfoResponse): void {
  if (data.coop_url === undefined)
    throw new SchemaValidationError("ServerInfoResponse.coop_url is undefined");
  if (data.coop_url === null)
    throw new SchemaValidationError("ServerInfoResponse.coop_url is null");
  if (data.coop_url.length < 1)
    throw new SchemaValidationError("ServerInfoResponse.coop_url is too short");
  if (data.total_sessions === undefined)
    throw new SchemaValidationError(
      "ServerInfoResponse.total_sessions is undefined"
    );
  if (data.total_sessions === null)
    throw new SchemaValidationError(
      "ServerInfoResponse.total_sessions is null"
    );
  if (data.total_sessions < 0)
    throw new SchemaValidationError(
      "ServerInfoResponse.total_sessions has a value below minimum"
    );
  if (data.total_users === undefined)
    throw new SchemaValidationError(
      "ServerInfoResponse.total_users is undefined"
    );
  if (data.total_users === null)
    throw new SchemaValidationError("ServerInfoResponse.total_users is null");
  if (data.total_users < 0)
    throw new SchemaValidationError(
      "ServerInfoResponse.total_users has a value below minimum"
    );
}
function validateSession(data: ISession): void {
  if (data.description === undefined)
    throw new SchemaValidationError("Session.description is undefined");
  if (data.description === null)
    throw new SchemaValidationError("Session.description is null");
  if (data.id === undefined)
    throw new SchemaValidationError("Session.id is undefined");
  if (data.id === null) throw new SchemaValidationError("Session.id is null");
  if (data.id.length < 1)
    throw new SchemaValidationError("Session.id is too short");
  if (data.owner === undefined)
    throw new SchemaValidationError("Session.owner is undefined");
  if (data.owner === null)
    throw new SchemaValidationError("Session.owner is null");
  if (data.owner.length < 1)
    throw new SchemaValidationError("Session.owner is too short");
  if (data.players === undefined)
    throw new SchemaValidationError("Session.players is undefined");
  if (data.players === null)
    throw new SchemaValidationError("Session.players is null");
  for (const fieldData of data.players) {
    if (fieldData === undefined)
      throw new SchemaValidationError("Session.players is undefined");
    if (fieldData === null)
      throw new SchemaValidationError("Session.players is null");
    if (fieldData.length < 1)
      throw new SchemaValidationError("Session.players is too short");
  }

  if (data.tags === undefined)
    throw new SchemaValidationError("Session.tags is undefined");
  if (data.tags === null)
    throw new SchemaValidationError("Session.tags is null");
  for (const fieldData of data.tags) {
    validateSessionTag(fieldData);
  }

  if (data.time === undefined)
    throw new SchemaValidationError("Session.time is undefined");
  if (data.time !== null) {
    validateTimeSpan(data.time);
  }
}
function validateSessionAccessRequest(data: ISessionAccessRequest): void {
  if (data.api_key === undefined)
    throw new SchemaValidationError(
      "SessionAccessRequest.api_key is undefined"
    );
  if (data.api_key === null)
    throw new SchemaValidationError("SessionAccessRequest.api_key is null");
  if (data.api_key.length < 1)
    throw new SchemaValidationError(
      "SessionAccessRequest.api_key is too short"
    );
  if (data.auth_token === undefined)
    throw new SchemaValidationError(
      "SessionAccessRequest.auth_token is undefined"
    );
  if (data.auth_token === null)
    throw new SchemaValidationError("SessionAccessRequest.auth_token is null");
  if (data.auth_token.length < 1)
    throw new SchemaValidationError(
      "SessionAccessRequest.auth_token is too short"
    );
  if (data.session_id === undefined)
    throw new SchemaValidationError(
      "SessionAccessRequest.session_id is undefined"
    );
  if (data.session_id === null)
    throw new SchemaValidationError("SessionAccessRequest.session_id is null");
  if (data.session_id.length < 1)
    throw new SchemaValidationError(
      "SessionAccessRequest.session_id is too short"
    );
  if (data.username === undefined)
    throw new SchemaValidationError(
      "SessionAccessRequest.username is undefined"
    );
  if (data.username === null)
    throw new SchemaValidationError("SessionAccessRequest.username is null");
  if (data.username.length < 1)
    throw new SchemaValidationError(
      "SessionAccessRequest.username is too short"
    );
}
function validateSessionPlayers(data: ISessionPlayers): void {
  if (data.session_id === undefined)
    throw new SchemaValidationError("SessionPlayers.session_id is undefined");
  if (data.session_id === null)
    throw new SchemaValidationError("SessionPlayers.session_id is null");
  if (data.session_id.length < 1)
    throw new SchemaValidationError("SessionPlayers.session_id is too short");
  if (data.usernames === undefined)
    throw new SchemaValidationError("SessionPlayers.usernames is undefined");
  if (data.usernames === null)
    throw new SchemaValidationError("SessionPlayers.usernames is null");
  for (const fieldData of data.usernames) {
    if (fieldData === undefined)
      throw new SchemaValidationError("SessionPlayers.usernames is undefined");
    if (fieldData === null)
      throw new SchemaValidationError("SessionPlayers.usernames is null");
    if (fieldData.length < 1)
      throw new SchemaValidationError("SessionPlayers.usernames is too short");
  }
}
function validateSessionResponse(data: ISessionResponse): void {
  if (data.session === undefined)
    throw new SchemaValidationError("SessionResponse.session is undefined");
  if (data.session !== null) {
    validateSession(data.session);
  }
}
function validateSessionTag(data: ISessionTag): void {
  if (data.description === undefined)
    throw new SchemaValidationError("SessionTag.description is undefined");
  if (data.description === null)
    throw new SchemaValidationError("SessionTag.description is null");
  if (data.description.length < 1)
    throw new SchemaValidationError("SessionTag.description is too short");
  if (data.name === undefined)
    throw new SchemaValidationError("SessionTag.name is undefined");
  if (data.name === null)
    throw new SchemaValidationError("SessionTag.name is null");
  if (data.name.length < 1)
    throw new SchemaValidationError("SessionTag.name is too short");
}
function validateSessionsPlayersRequest(data: ISessionsPlayersRequest): void {
  if (data.api_key === undefined)
    throw new SchemaValidationError(
      "SessionsPlayersRequest.api_key is undefined"
    );
  if (data.api_key === null)
    throw new SchemaValidationError("SessionsPlayersRequest.api_key is null");
  if (data.api_key.length < 1)
    throw new SchemaValidationError(
      "SessionsPlayersRequest.api_key is too short"
    );
  if (data.sessions === undefined)
    throw new SchemaValidationError(
      "SessionsPlayersRequest.sessions is undefined"
    );
  if (data.sessions === null)
    throw new SchemaValidationError("SessionsPlayersRequest.sessions is null");
  for (const fieldData of data.sessions) {
    validateSessionPlayers(fieldData);
  }
}
function validateSessionsResponse(data: ISessionsResponse): void {
  if (data.sessions === undefined)
    throw new SchemaValidationError("SessionsResponse.sessions is undefined");
  if (data.sessions === null)
    throw new SchemaValidationError("SessionsResponse.sessions is null");
  for (const fieldData of data.sessions) {
    validateSession(fieldData);
  }
}
function validateSuccessResponse(data: ISuccessResponse): void {
  if (data.message === undefined)
    throw new SchemaValidationError("SuccessResponse.message is undefined");
  if (data.message === null)
    throw new SchemaValidationError("SuccessResponse.message is null");
  if (data.success === undefined)
    throw new SchemaValidationError("SuccessResponse.success is undefined");
  if (data.success === null)
    throw new SchemaValidationError("SuccessResponse.success is null");
}
function validateTag(data: ITag): void {
  if (data.description === undefined)
    throw new SchemaValidationError("Tag.description is undefined");
  if (data.description === null)
    throw new SchemaValidationError("Tag.description is null");
  if (data.id === undefined)
    throw new SchemaValidationError("Tag.id is undefined");
  if (data.id === null) throw new SchemaValidationError("Tag.id is null");
  if (data.name === undefined)
    throw new SchemaValidationError("Tag.name is undefined");
  if (data.name === null) throw new SchemaValidationError("Tag.name is null");
  if (data.name.length < 1)
    throw new SchemaValidationError("Tag.name is too short");
}
function validateTagsResponse(data: ITagsResponse): void {
  if (data.tags === undefined)
    throw new SchemaValidationError("TagsResponse.tags is undefined");
  if (data.tags === null)
    throw new SchemaValidationError("TagsResponse.tags is null");
  for (const fieldData of data.tags) {
    validateTag(fieldData);
  }
}
function validateTimeSpan(data: ITimeSpan): void {
  if (data.end === undefined)
    throw new SchemaValidationError("TimeSpan.end is undefined");
  if (data.end === null)
    throw new SchemaValidationError("TimeSpan.end is null");
  if (
    !data.end.match(
      /^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]+(\+[0-9]{2}:[0-9]{2}|Z)$/
    )
  )
    throw new SchemaValidationError("TimeSpan.end has an invalid format");
  if (data.start === undefined)
    throw new SchemaValidationError("TimeSpan.start is undefined");
  if (data.start === null)
    throw new SchemaValidationError("TimeSpan.start is null");
  if (
    !data.start.match(
      /^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]+(\+[0-9]{2}:[0-9]{2}|Z)$/
    )
  )
    throw new SchemaValidationError("TimeSpan.start has an invalid format");
}
export async function getServerInfo(): Promise<IServerInfoResponse> {
  const result = (await doGet(`/api/v0/server-info`)) as IServerInfoResponse;
  validateServerInfoResponse(result);
  return result;
}
export async function getTags(): Promise<ITagsResponse> {
  const result = (await doGet(`/api/v0/tags`)) as ITagsResponse;
  validateTagsResponse(result);
  return result;
}
export async function getSessions(): Promise<ISessionsResponse> {
  const result = (await doGet(`/api/v0/sessions`)) as ISessionsResponse;
  validateSessionsResponse(result);
  return result;
}
export async function createSession(
  body: ICreateSessionRequest
): Promise<ISuccessResponse> {
  validateCreateSessionRequest(body);
  const result = (await doPost(`/api/v0/sessions`, body)) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}
export async function getSession(sessionId: string): Promise<ISessionResponse> {
  const result = (await doGet(
    `/api/v0/sessions/${encodeURIComponent(sessionId)}`
  )) as ISessionResponse;
  validateSessionResponse(result);
  return result;
}
export async function editSession(
  sessionId: string,
  body: ICreateSessionRequest
): Promise<ISuccessResponse> {
  validateCreateSessionRequest(body);
  const result = (await doPost(
    `/api/v0/sessions/${encodeURIComponent(sessionId)}`,
    body
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}
export async function deleteSession(
  sessionId: string
): Promise<ISuccessResponse> {
  const result = (await doDelete(
    `/api/v0/sessions/${encodeURIComponent(sessionId)}`
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}
export async function checkSessionAccess(
  body: ISessionAccessRequest
): Promise<ISuccessResponse> {
  validateSessionAccessRequest(body);
  const result = (await doPost(
    `/api/v0/sessions/check-access`,
    body
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}
export async function updateSessionsPlayers(
  body: ISessionsPlayersRequest
): Promise<IEmpty> {
  validateSessionsPlayersRequest(body);
  const result = (await doPost(
    `/api/v0/sessions/session-players`,
    body
  )) as IEmpty;
  validateEmpty(result);
  return result;
}
export async function getAnnouncements(): Promise<IAnnouncementsResponse> {
  const result = (await doGet(
    `/api/v0/announcements`
  )) as IAnnouncementsResponse;
  validateAnnouncementsResponse(result);
  return result;
}
export async function getProfile(): Promise<IProfileInfoResponse> {
  const result = (await doGet(`/api/v0/auth/profile`)) as IProfileInfoResponse;
  validateProfileInfoResponse(result);
  return result;
}
export async function changeUsername(
  body: IChangeUsernameRequest
): Promise<ISuccessResponse> {
  validateChangeUsernameRequest(body);
  const result = (await doPost(
    `/api/v0/auth/change-username`,
    body
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}
export async function regenerateToken(): Promise<IEmpty> {
  const result = (await doGet(`/api/v0/auth/regenerate-token`)) as IEmpty;
  validateEmpty(result);
  return result;
}
export async function login(body: ILoginRequest): Promise<ISuccessResponse> {
  validateLoginRequest(body);
  const result = (await doPost(`/api/v0/auth/login`, body)) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}
export async function register(
  body: IRegisterRequest
): Promise<ISuccessResponse> {
  validateRegisterRequest(body);
  const result = (await doPost(
    `/api/v0/auth/register`,
    body
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}
export async function changePassword(
  body: IChangePasswordRequest
): Promise<ISuccessResponse> {
  validateChangePasswordRequest(body);
  const result = (await doPost(
    `/api/v0/auth/change-password`,
    body
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}
export async function changeEmail(
  body: IChangeEmailRequest
): Promise<ISuccessResponse> {
  validateChangeEmailRequest(body);
  const result = (await doPost(
    `/api/v0/auth/change-email`,
    body
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}
export async function logout(): Promise<IEmpty> {
  const result = (await doGet(`/api/v0/auth/logout`)) as IEmpty;
  validateEmpty(result);
  return result;
}
function getCookie(name: string): string | null {
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (const cookie of cookies) {
      // Does this cookie string begin with the name we want?
      if (cookie.trim().startsWith(name + "=")) {
        return decodeURIComponent(cookie.trim().substring(name.length + 1));
      }
    }
  }
  return null;
}

function getCsrfHeader(): Headers {
  const csrftoken = getCookie("csrftoken");
  const headers = new Headers();
  if (csrftoken != null) headers.append("X-CSRFToken", csrftoken);
  return headers;
}

export async function doGet(url: string): Promise<object> {
  return await fetch(`${process.env.VUE_APP_SERVER_URL}${url}`, {
    credentials: "include",
    headers: getCsrfHeader(),
  }).then((r) => r.json());
}

export async function doDelete(url: string): Promise<object> {
  return await fetch(`${process.env.VUE_APP_SERVER_URL}${url}`, {
    method: "DELETE",
    credentials: "include",
    headers: getCsrfHeader(),
  }).then((r) => r.json());
}

export async function doPost(url: string, body: object): Promise<object> {
  return await fetch(`${process.env.VUE_APP_SERVER_URL}${url}`, {
    method: "POST",
    credentials: "include",
    headers: getCsrfHeader(),
    body: JSON.stringify(body),
  }).then((r) => r.json());
}

export class SchemaValidationError implements Error {
  public constructor(public readonly message: string) {
    this.name = "SchemaValidationError";
  }

  name: string;
}
