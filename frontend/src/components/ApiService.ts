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
}
export interface IDeleteSessionRequest {
  session_id: string;
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
  username: string;
  verified: boolean;
}
export interface IRegisterRequest {
  email: string;
  password: string;
  username: string;
}
export interface ISession {
  description: string;
  id: string;
  owner: string;
  players: string[];
  tags: ISessionTag[];
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
export interface IStatsResponse {
  total_sessions: number;
  total_users: number;
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
function validateAnnouncementEntry(data: IAnnouncementEntry): void {
  if (data.background_color === undefined)
    throw new SchemaValidationError("AnnouncementEntry.background_color");
  if (data.background_color === null)
    throw new SchemaValidationError("AnnouncementEntry.background_color");
  if (data.background_color.length < 1)
    throw new SchemaValidationError("AnnouncementEntry.background_color");
  if (data.message === undefined)
    throw new SchemaValidationError("AnnouncementEntry.message");
  if (data.message === null)
    throw new SchemaValidationError("AnnouncementEntry.message");
  if (data.message.length < 1)
    throw new SchemaValidationError("AnnouncementEntry.message");
  if (data.text_color === undefined)
    throw new SchemaValidationError("AnnouncementEntry.text_color");
  if (data.text_color === null)
    throw new SchemaValidationError("AnnouncementEntry.text_color");
  if (data.text_color.length < 1)
    throw new SchemaValidationError("AnnouncementEntry.text_color");
}
function validateAnnouncementsResponse(data: IAnnouncementsResponse): void {
  if (data.announcements === undefined)
    throw new SchemaValidationError("AnnouncementsResponse.announcements");
  if (data.announcements === null)
    throw new SchemaValidationError("AnnouncementsResponse.announcements");
  for (const fieldData of data.announcements) {
    validateAnnouncementEntry(fieldData);
  }
}
function validateChangeEmailRequest(data: IChangeEmailRequest): void {
  if (data.email === undefined)
    throw new SchemaValidationError("ChangeEmailRequest.email");
  if (data.email === null)
    throw new SchemaValidationError("ChangeEmailRequest.email");
  if (data.email.length < 1)
    throw new SchemaValidationError("ChangeEmailRequest.email");
}
function validateChangePasswordRequest(data: IChangePasswordRequest): void {
  if (data.password === undefined)
    throw new SchemaValidationError("ChangePasswordRequest.password");
  if (data.password === null)
    throw new SchemaValidationError("ChangePasswordRequest.password");
  if (data.password.length < 1)
    throw new SchemaValidationError("ChangePasswordRequest.password");
}
function validateChangeUsernameRequest(data: IChangeUsernameRequest): void {
  if (data.username === undefined)
    throw new SchemaValidationError("ChangeUsernameRequest.username");
  if (data.username === null)
    throw new SchemaValidationError("ChangeUsernameRequest.username");
  if (data.username.length < 1)
    throw new SchemaValidationError("ChangeUsernameRequest.username");
}
function validateCreateSessionRequest(data: ICreateSessionRequest): void {
  if (data.description === undefined)
    throw new SchemaValidationError("CreateSessionRequest.description");
  if (data.description === null)
    throw new SchemaValidationError("CreateSessionRequest.description");
  if (data.tags === undefined)
    throw new SchemaValidationError("CreateSessionRequest.tags");
  if (data.tags === null)
    throw new SchemaValidationError("CreateSessionRequest.tags");
  for (const fieldData of data.tags) {
    if (fieldData === undefined)
      throw new SchemaValidationError("CreateSessionRequest.tags");
    if (fieldData === null)
      throw new SchemaValidationError("CreateSessionRequest.tags");
  }
}
function validateDeleteSessionRequest(data: IDeleteSessionRequest): void {
  if (data.session_id === undefined)
    throw new SchemaValidationError("DeleteSessionRequest.session_id");
  if (data.session_id === null)
    throw new SchemaValidationError("DeleteSessionRequest.session_id");
  if (data.session_id.length < 1)
    throw new SchemaValidationError("DeleteSessionRequest.session_id");
}
function validateEmpty(data: IEmpty): void {}
function validateLoginRequest(data: ILoginRequest): void {
  if (data.password === undefined)
    throw new SchemaValidationError("LoginRequest.password");
  if (data.password === null)
    throw new SchemaValidationError("LoginRequest.password");
  if (data.password.length < 1)
    throw new SchemaValidationError("LoginRequest.password");
  if (data.username === undefined)
    throw new SchemaValidationError("LoginRequest.username");
  if (data.username === null)
    throw new SchemaValidationError("LoginRequest.username");
  if (data.username.length < 1)
    throw new SchemaValidationError("LoginRequest.username");
}
function validateProfileInfoResponse(data: IProfileInfoResponse): void {
  if (data.auth_token === undefined)
    throw new SchemaValidationError("ProfileInfoResponse.auth_token");
  if (data.auth_token !== null) {
    if (data.auth_token.length < 1)
      throw new SchemaValidationError("ProfileInfoResponse.auth_token");
  }
  if (data.authenticated === undefined)
    throw new SchemaValidationError("ProfileInfoResponse.authenticated");
  if (data.authenticated === null)
    throw new SchemaValidationError("ProfileInfoResponse.authenticated");
  if (data.email === undefined)
    throw new SchemaValidationError("ProfileInfoResponse.email");
  if (data.email !== null) {
    if (data.email.length < 1)
      throw new SchemaValidationError("ProfileInfoResponse.email");
  }
  if (data.username === undefined)
    throw new SchemaValidationError("ProfileInfoResponse.username");
  if (data.username === null)
    throw new SchemaValidationError("ProfileInfoResponse.username");
  if (data.username.length < 1)
    throw new SchemaValidationError("ProfileInfoResponse.username");
  if (data.verified === undefined)
    throw new SchemaValidationError("ProfileInfoResponse.verified");
  if (data.verified === null)
    throw new SchemaValidationError("ProfileInfoResponse.verified");
}
function validateRegisterRequest(data: IRegisterRequest): void {
  if (data.email === undefined)
    throw new SchemaValidationError("RegisterRequest.email");
  if (data.email === null)
    throw new SchemaValidationError("RegisterRequest.email");
  if (data.email.length < 1)
    throw new SchemaValidationError("RegisterRequest.email");
  if (data.password === undefined)
    throw new SchemaValidationError("RegisterRequest.password");
  if (data.password === null)
    throw new SchemaValidationError("RegisterRequest.password");
  if (data.password.length < 1)
    throw new SchemaValidationError("RegisterRequest.password");
  if (data.username === undefined)
    throw new SchemaValidationError("RegisterRequest.username");
  if (data.username === null)
    throw new SchemaValidationError("RegisterRequest.username");
  if (data.username.length < 1)
    throw new SchemaValidationError("RegisterRequest.username");
}
function validateSession(data: ISession): void {
  if (data.description === undefined)
    throw new SchemaValidationError("Session.description");
  if (data.description === null)
    throw new SchemaValidationError("Session.description");
  if (data.id === undefined) throw new SchemaValidationError("Session.id");
  if (data.id === null) throw new SchemaValidationError("Session.id");
  if (data.id.length < 1) throw new SchemaValidationError("Session.id");
  if (data.owner === undefined)
    throw new SchemaValidationError("Session.owner");
  if (data.owner === null) throw new SchemaValidationError("Session.owner");
  if (data.owner.length < 1) throw new SchemaValidationError("Session.owner");
  if (data.players === undefined)
    throw new SchemaValidationError("Session.players");
  if (data.players === null) throw new SchemaValidationError("Session.players");
  for (const fieldData of data.players) {
    if (fieldData === undefined)
      throw new SchemaValidationError("Session.players");
    if (fieldData === null) throw new SchemaValidationError("Session.players");
    if (fieldData.length < 1)
      throw new SchemaValidationError("Session.players");
  }

  if (data.tags === undefined) throw new SchemaValidationError("Session.tags");
  if (data.tags === null) throw new SchemaValidationError("Session.tags");
  for (const fieldData of data.tags) {
    validateSessionTag(fieldData);
  }
}
function validateSessionAccessRequest(data: ISessionAccessRequest): void {
  if (data.api_key === undefined)
    throw new SchemaValidationError("SessionAccessRequest.api_key");
  if (data.api_key === null)
    throw new SchemaValidationError("SessionAccessRequest.api_key");
  if (data.api_key.length < 1)
    throw new SchemaValidationError("SessionAccessRequest.api_key");
  if (data.auth_token === undefined)
    throw new SchemaValidationError("SessionAccessRequest.auth_token");
  if (data.auth_token === null)
    throw new SchemaValidationError("SessionAccessRequest.auth_token");
  if (data.auth_token.length < 1)
    throw new SchemaValidationError("SessionAccessRequest.auth_token");
  if (data.session_id === undefined)
    throw new SchemaValidationError("SessionAccessRequest.session_id");
  if (data.session_id === null)
    throw new SchemaValidationError("SessionAccessRequest.session_id");
  if (data.session_id.length < 1)
    throw new SchemaValidationError("SessionAccessRequest.session_id");
  if (data.username === undefined)
    throw new SchemaValidationError("SessionAccessRequest.username");
  if (data.username === null)
    throw new SchemaValidationError("SessionAccessRequest.username");
  if (data.username.length < 1)
    throw new SchemaValidationError("SessionAccessRequest.username");
}
function validateSessionPlayers(data: ISessionPlayers): void {
  if (data.session_id === undefined)
    throw new SchemaValidationError("SessionPlayers.session_id");
  if (data.session_id === null)
    throw new SchemaValidationError("SessionPlayers.session_id");
  if (data.session_id.length < 1)
    throw new SchemaValidationError("SessionPlayers.session_id");
  if (data.usernames === undefined)
    throw new SchemaValidationError("SessionPlayers.usernames");
  if (data.usernames === null)
    throw new SchemaValidationError("SessionPlayers.usernames");
  for (const fieldData of data.usernames) {
    if (fieldData === undefined)
      throw new SchemaValidationError("SessionPlayers.usernames");
    if (fieldData === null)
      throw new SchemaValidationError("SessionPlayers.usernames");
    if (fieldData.length < 1)
      throw new SchemaValidationError("SessionPlayers.usernames");
  }
}
function validateSessionTag(data: ISessionTag): void {
  if (data.description === undefined)
    throw new SchemaValidationError("SessionTag.description");
  if (data.description === null)
    throw new SchemaValidationError("SessionTag.description");
  if (data.description.length < 1)
    throw new SchemaValidationError("SessionTag.description");
  if (data.name === undefined)
    throw new SchemaValidationError("SessionTag.name");
  if (data.name === null) throw new SchemaValidationError("SessionTag.name");
  if (data.name.length < 1) throw new SchemaValidationError("SessionTag.name");
}
function validateSessionsPlayersRequest(data: ISessionsPlayersRequest): void {
  if (data.api_key === undefined)
    throw new SchemaValidationError("SessionsPlayersRequest.api_key");
  if (data.api_key === null)
    throw new SchemaValidationError("SessionsPlayersRequest.api_key");
  if (data.api_key.length < 1)
    throw new SchemaValidationError("SessionsPlayersRequest.api_key");
  if (data.sessions === undefined)
    throw new SchemaValidationError("SessionsPlayersRequest.sessions");
  if (data.sessions === null)
    throw new SchemaValidationError("SessionsPlayersRequest.sessions");
  for (const fieldData of data.sessions) {
    validateSessionPlayers(fieldData);
  }
}
function validateSessionsResponse(data: ISessionsResponse): void {
  if (data.sessions === undefined)
    throw new SchemaValidationError("SessionsResponse.sessions");
  if (data.sessions === null)
    throw new SchemaValidationError("SessionsResponse.sessions");
  for (const fieldData of data.sessions) {
    validateSession(fieldData);
  }
}
function validateStatsResponse(data: IStatsResponse): void {
  if (data.total_sessions === undefined)
    throw new SchemaValidationError("StatsResponse.total_sessions");
  if (data.total_sessions === null)
    throw new SchemaValidationError("StatsResponse.total_sessions");
  if (data.total_sessions < 0)
    throw new SchemaValidationError("StatsResponse.total_sessions");
  if (data.total_users === undefined)
    throw new SchemaValidationError("StatsResponse.total_users");
  if (data.total_users === null)
    throw new SchemaValidationError("StatsResponse.total_users");
  if (data.total_users < 0)
    throw new SchemaValidationError("StatsResponse.total_users");
}
function validateSuccessResponse(data: ISuccessResponse): void {
  if (data.message === undefined)
    throw new SchemaValidationError("SuccessResponse.message");
  if (data.message === null)
    throw new SchemaValidationError("SuccessResponse.message");
  if (data.success === undefined)
    throw new SchemaValidationError("SuccessResponse.success");
  if (data.success === null)
    throw new SchemaValidationError("SuccessResponse.success");
}
function validateTag(data: ITag): void {
  if (data.description === undefined)
    throw new SchemaValidationError("Tag.description");
  if (data.description === null)
    throw new SchemaValidationError("Tag.description");
  if (data.id === undefined) throw new SchemaValidationError("Tag.id");
  if (data.id === null) throw new SchemaValidationError("Tag.id");
  if (data.name === undefined) throw new SchemaValidationError("Tag.name");
  if (data.name === null) throw new SchemaValidationError("Tag.name");
  if (data.name.length < 1) throw new SchemaValidationError("Tag.name");
}
function validateTagsResponse(data: ITagsResponse): void {
  if (data.tags === undefined)
    throw new SchemaValidationError("TagsResponse.tags");
  if (data.tags === null) throw new SchemaValidationError("TagsResponse.tags");
  for (const fieldData of data.tags) {
    validateTag(fieldData);
  }
}
export async function getStats(): Promise<IStatsResponse> {
  const result = (await get("/api/v0/stats")) as IStatsResponse;
  validateStatsResponse(result);
  return result;
}
export async function getTags(): Promise<ITagsResponse> {
  const result = (await get("/api/v0/tags")) as ITagsResponse;
  validateTagsResponse(result);
  return result;
}
export async function getSessions(): Promise<ISessionsResponse> {
  const result = (await get("/api/v0/sessions")) as ISessionsResponse;
  validateSessionsResponse(result);
  return result;
}
export async function createSession(
  body: ICreateSessionRequest
): Promise<ISuccessResponse> {
  validateCreateSessionRequest(body);
  const result = (await post(
    "/api/v0/sessions/create",
    body
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}
export async function deleteSession(
  body: IDeleteSessionRequest
): Promise<ISuccessResponse> {
  validateDeleteSessionRequest(body);
  const result = (await post(
    "/api/v0/sessions/delete",
    body
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}
export async function checkSessionAccess(
  body: ISessionAccessRequest
): Promise<ISuccessResponse> {
  validateSessionAccessRequest(body);
  const result = (await post(
    "/api/v0/sessions/check-access",
    body
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}
export async function updateSessionsPlayers(
  body: ISessionsPlayersRequest
): Promise<IEmpty> {
  validateSessionsPlayersRequest(body);
  const result = (await post(
    "/api/v0/sessions/session-players",
    body
  )) as IEmpty;
  validateEmpty(result);
  return result;
}
export async function getAnnouncements(): Promise<IAnnouncementsResponse> {
  const result = (await get("/api/v0/announcements")) as IAnnouncementsResponse;
  validateAnnouncementsResponse(result);
  return result;
}
export async function getProfile(): Promise<IProfileInfoResponse> {
  const result = (await get("/api/v0/auth/profile")) as IProfileInfoResponse;
  validateProfileInfoResponse(result);
  return result;
}
export async function changeUsername(
  body: IChangeUsernameRequest
): Promise<ISuccessResponse> {
  validateChangeUsernameRequest(body);
  const result = (await post(
    "/api/v0/auth/change-username",
    body
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}
export async function regenerateToken(): Promise<IEmpty> {
  const result = (await get("/api/v0/auth/regenerate-token")) as IEmpty;
  validateEmpty(result);
  return result;
}
export async function login(body: ILoginRequest): Promise<ISuccessResponse> {
  validateLoginRequest(body);
  const result = (await post("/api/v0/auth/login", body)) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}
export async function register(
  body: IRegisterRequest
): Promise<ISuccessResponse> {
  validateRegisterRequest(body);
  const result = (await post(
    "/api/v0/auth/register",
    body
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}
export async function changePassword(
  body: IChangePasswordRequest
): Promise<ISuccessResponse> {
  validateChangePasswordRequest(body);
  const result = (await post(
    "/api/v0/auth/change-password",
    body
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}
export async function changeEmail(
  body: IChangeEmailRequest
): Promise<ISuccessResponse> {
  validateChangeEmailRequest(body);
  const result = (await post(
    "/api/v0/auth/change-email",
    body
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}
export async function logout(): Promise<IEmpty> {
  const result = (await get("/api/v0/auth/logout")) as IEmpty;
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

export async function get(url: string): Promise<object> {
  return await fetch(`${process.env.VUE_APP_SERVER_URL}${url}`, {
    credentials: "include",
    headers: getCsrfHeader(),
  }).then((r) => r.json());
}

export async function post(url: string, body: object): Promise<object> {
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
