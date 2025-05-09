/* eslint-disable @typescript-eslint/no-unused-vars */

const env = await import.meta.env;

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
  private: boolean;
  tags: number[];
  time: ITimeSpan | null;
}

export type IEmpty = object;

export interface IGhostFileResponse {
  ghost: IGhostFileResponseEntry | null;
}

export interface IGhostFileResponseEntry {
  description: string;
  downloads: number;
  duration: number;
  finish_type: string;
  id: number;
  level_display: string;
  level_id: number;
  level_identifier: string;
  published: boolean;
  size: number;
  tags: ITag[];
  username: string;
}

export interface IGhostFilesResponse {
  files: IGhostFileResponseEntry[];
}

export interface IGhostInfoRequest {
  description: string;
  level_id: number;
  published: boolean;
  tags: number[];
}

export interface ILevelInfo {
  id: number;
  identifier: string;
  title: string;
}

export interface ILevelsResponse {
  levels: ILevelInfo[];
}

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
}

export interface IQuotaResponse {
  current: number;
  max: number;
}

export interface IRegisterRequest {
  email: string;
  password: string;
  username: string;
}

export interface IServerInfoResponse {
  coop_url: string;
  total_ghost_duration: number;
  total_ghosts: number;
  total_sessions: number;
  total_users: number;
}

export interface ISession {
  description: string;
  id: string;
  owner: string;
  players: string[];
  private: boolean;
  tags: ITag[];
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
  if (data.background_color === undefined) {
    throw new SchemaValidationError(
      "AnnouncementEntry.background_color is undefined",
    );
  }
  if (data.background_color === null) {
    throw new SchemaValidationError(
      "AnnouncementEntry.background_color is null",
    );
  }
  if (data.background_color.length < 1) {
    throw new SchemaValidationError(
      "AnnouncementEntry.background_color is too short",
    );
  }
  if (data.message === undefined) {
    throw new SchemaValidationError("AnnouncementEntry.message is undefined");
  }
  if (data.message === null) {
    throw new SchemaValidationError("AnnouncementEntry.message is null");
  }
  if (data.message.length < 1) {
    throw new SchemaValidationError("AnnouncementEntry.message is too short");
  }
  if (data.text_color === undefined) {
    throw new SchemaValidationError(
      "AnnouncementEntry.text_color is undefined",
    );
  }
  if (data.text_color === null) {
    throw new SchemaValidationError("AnnouncementEntry.text_color is null");
  }
  if (data.text_color.length < 1) {
    throw new SchemaValidationError(
      "AnnouncementEntry.text_color is too short",
    );
  }
}

function validateAnnouncementsResponse(data: IAnnouncementsResponse): void {
  if (data.announcements === undefined) {
    throw new SchemaValidationError(
      "AnnouncementsResponse.announcements is undefined",
    );
  }
  if (data.announcements === null) {
    throw new SchemaValidationError(
      "AnnouncementsResponse.announcements is null",
    );
  }
  for (const fieldData of data.announcements) {
    validateAnnouncementEntry(fieldData);
  }
}

function validateChangeEmailRequest(data: IChangeEmailRequest): void {
  if (data.email === undefined) {
    throw new SchemaValidationError("ChangeEmailRequest.email is undefined");
  }
  if (data.email === null) {
    throw new SchemaValidationError("ChangeEmailRequest.email is null");
  }
  if (data.email.length < 1) {
    throw new SchemaValidationError("ChangeEmailRequest.email is too short");
  }
}

function validateChangePasswordRequest(data: IChangePasswordRequest): void {
  if (data.password === undefined) {
    throw new SchemaValidationError(
      "ChangePasswordRequest.password is undefined",
    );
  }
  if (data.password === null) {
    throw new SchemaValidationError("ChangePasswordRequest.password is null");
  }
  if (data.password.length < 1) {
    throw new SchemaValidationError(
      "ChangePasswordRequest.password is too short",
    );
  }
}

function validateChangeUsernameRequest(data: IChangeUsernameRequest): void {
  if (data.username === undefined) {
    throw new SchemaValidationError(
      "ChangeUsernameRequest.username is undefined",
    );
  }
  if (data.username === null) {
    throw new SchemaValidationError("ChangeUsernameRequest.username is null");
  }
  if (data.username.length < 1) {
    throw new SchemaValidationError(
      "ChangeUsernameRequest.username is too short",
    );
  }
}

function validateCreateSessionRequest(data: ICreateSessionRequest): void {
  if (data.description === undefined) {
    throw new SchemaValidationError(
      "CreateSessionRequest.description is undefined",
    );
  }
  if (data.description === null) {
    throw new SchemaValidationError("CreateSessionRequest.description is null");
  }
  if (data.description.length > 512) {
    throw new SchemaValidationError(
      "CreateSessionRequest.description is too long",
    );
  }
  if (data.private === undefined) {
    throw new SchemaValidationError(
      "CreateSessionRequest.private is undefined",
    );
  }
  if (data.private === null) {
    throw new SchemaValidationError("CreateSessionRequest.private is null");
  }
  if (data.tags === undefined) {
    throw new SchemaValidationError("CreateSessionRequest.tags is undefined");
  }
  if (data.tags === null) {
    throw new SchemaValidationError("CreateSessionRequest.tags is null");
  }
  for (const fieldData of data.tags) {
    if (fieldData === undefined) {
      throw new SchemaValidationError("CreateSessionRequest.tags is undefined");
    }
    if (fieldData === null) {
      throw new SchemaValidationError("CreateSessionRequest.tags is null");
    }
  }

  if (data.time === undefined) {
    throw new SchemaValidationError("CreateSessionRequest.time is undefined");
  }
  if (data.time !== null) {
    validateTimeSpan(data.time);
  }
}

function validateEmpty(data: IEmpty): void {}

function validateGhostFileResponse(data: IGhostFileResponse): void {
  if (data.ghost === undefined) {
    throw new SchemaValidationError("GhostFileResponse.ghost is undefined");
  }
  if (data.ghost !== null) {
    validateGhostFileResponseEntry(data.ghost);
  }
}

function validateGhostFileResponseEntry(data: IGhostFileResponseEntry): void {
  if (data.description === undefined) {
    throw new SchemaValidationError(
      "GhostFileResponseEntry.description is undefined",
    );
  }
  if (data.description === null) {
    throw new SchemaValidationError(
      "GhostFileResponseEntry.description is null",
    );
  }
  if (data.downloads === undefined) {
    throw new SchemaValidationError(
      "GhostFileResponseEntry.downloads is undefined",
    );
  }
  if (data.downloads === null) {
    throw new SchemaValidationError("GhostFileResponseEntry.downloads is null");
  }
  if (data.downloads < 0) {
    throw new SchemaValidationError(
      "GhostFileResponseEntry.downloads has a value below minimum",
    );
  }
  if (data.duration === undefined) {
    throw new SchemaValidationError(
      "GhostFileResponseEntry.duration is undefined",
    );
  }
  if (data.duration === null) {
    throw new SchemaValidationError("GhostFileResponseEntry.duration is null");
  }
  if (data.duration < 0) {
    throw new SchemaValidationError(
      "GhostFileResponseEntry.duration has a value below minimum",
    );
  }
  if (data.finish_type === undefined) {
    throw new SchemaValidationError(
      "GhostFileResponseEntry.finish_type is undefined",
    );
  }
  if (data.finish_type === null) {
    throw new SchemaValidationError(
      "GhostFileResponseEntry.finish_type is null",
    );
  }
  if (data.id === undefined) {
    throw new SchemaValidationError("GhostFileResponseEntry.id is undefined");
  }
  if (data.id === null) {
    throw new SchemaValidationError("GhostFileResponseEntry.id is null");
  }
  if (data.level_display === undefined) {
    throw new SchemaValidationError(
      "GhostFileResponseEntry.level_display is undefined",
    );
  }
  if (data.level_display === null) {
    throw new SchemaValidationError(
      "GhostFileResponseEntry.level_display is null",
    );
  }
  if (data.level_display.length < 1) {
    throw new SchemaValidationError(
      "GhostFileResponseEntry.level_display is too short",
    );
  }
  if (data.level_id === undefined) {
    throw new SchemaValidationError(
      "GhostFileResponseEntry.level_id is undefined",
    );
  }
  if (data.level_id === null) {
    throw new SchemaValidationError("GhostFileResponseEntry.level_id is null");
  }
  if (data.level_identifier === undefined) {
    throw new SchemaValidationError(
      "GhostFileResponseEntry.level_identifier is undefined",
    );
  }
  if (data.level_identifier === null) {
    throw new SchemaValidationError(
      "GhostFileResponseEntry.level_identifier is null",
    );
  }
  if (data.level_identifier.length < 1) {
    throw new SchemaValidationError(
      "GhostFileResponseEntry.level_identifier is too short",
    );
  }
  if (data.published === undefined) {
    throw new SchemaValidationError(
      "GhostFileResponseEntry.published is undefined",
    );
  }
  if (data.published === null) {
    throw new SchemaValidationError("GhostFileResponseEntry.published is null");
  }
  if (data.size === undefined) {
    throw new SchemaValidationError("GhostFileResponseEntry.size is undefined");
  }
  if (data.size === null) {
    throw new SchemaValidationError("GhostFileResponseEntry.size is null");
  }
  if (data.size < 0) {
    throw new SchemaValidationError(
      "GhostFileResponseEntry.size has a value below minimum",
    );
  }
  if (data.tags === undefined) {
    throw new SchemaValidationError("GhostFileResponseEntry.tags is undefined");
  }
  if (data.tags === null) {
    throw new SchemaValidationError("GhostFileResponseEntry.tags is null");
  }
  for (const fieldData of data.tags) {
    validateTag(fieldData);
  }

  if (data.username === undefined) {
    throw new SchemaValidationError(
      "GhostFileResponseEntry.username is undefined",
    );
  }
  if (data.username === null) {
    throw new SchemaValidationError("GhostFileResponseEntry.username is null");
  }
  if (data.username.length < 1) {
    throw new SchemaValidationError(
      "GhostFileResponseEntry.username is too short",
    );
  }
}

function validateGhostFilesResponse(data: IGhostFilesResponse): void {
  if (data.files === undefined) {
    throw new SchemaValidationError("GhostFilesResponse.files is undefined");
  }
  if (data.files === null) {
    throw new SchemaValidationError("GhostFilesResponse.files is null");
  }
  for (const fieldData of data.files) {
    validateGhostFileResponseEntry(fieldData);
  }
}

function validateGhostInfoRequest(data: IGhostInfoRequest): void {
  if (data.description === undefined) {
    throw new SchemaValidationError(
      "GhostInfoRequest.description is undefined",
    );
  }
  if (data.description === null) {
    throw new SchemaValidationError("GhostInfoRequest.description is null");
  }
  if (data.level_id === undefined) {
    throw new SchemaValidationError("GhostInfoRequest.level_id is undefined");
  }
  if (data.level_id === null) {
    throw new SchemaValidationError("GhostInfoRequest.level_id is null");
  }
  if (data.published === undefined) {
    throw new SchemaValidationError("GhostInfoRequest.published is undefined");
  }
  if (data.published === null) {
    throw new SchemaValidationError("GhostInfoRequest.published is null");
  }
  if (data.tags === undefined) {
    throw new SchemaValidationError("GhostInfoRequest.tags is undefined");
  }
  if (data.tags === null) {
    throw new SchemaValidationError("GhostInfoRequest.tags is null");
  }
  for (const fieldData of data.tags) {
    if (fieldData === undefined) {
      throw new SchemaValidationError("GhostInfoRequest.tags is undefined");
    }
    if (fieldData === null) {
      throw new SchemaValidationError("GhostInfoRequest.tags is null");
    }
  }
}

function validateIsoDateTime(data?: string | null): void {
  if (data === undefined) {
    throw new SchemaValidationError("IsoDateTime is undefined");
  }
  if (data === null) {
    throw new SchemaValidationError("IsoDateTime is null");
  }
  if (
    !data.match(
      /^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?(\+[0-9]{2}:[0-9]{2}|Z)$/,
    )
  ) {
    throw new SchemaValidationError("IsoDateTime has an invalid format");
  }
}

function validateLevelInfo(data: ILevelInfo): void {
  if (data.id === undefined) {
    throw new SchemaValidationError("LevelInfo.id is undefined");
  }
  if (data.id === null) {
    throw new SchemaValidationError("LevelInfo.id is null");
  }
  if (data.identifier === undefined) {
    throw new SchemaValidationError("LevelInfo.identifier is undefined");
  }
  if (data.identifier === null) {
    throw new SchemaValidationError("LevelInfo.identifier is null");
  }
  if (data.identifier.length < 1) {
    throw new SchemaValidationError("LevelInfo.identifier is too short");
  }
  if (data.title === undefined) {
    throw new SchemaValidationError("LevelInfo.title is undefined");
  }
  if (data.title === null) {
    throw new SchemaValidationError("LevelInfo.title is null");
  }
  if (data.title.length < 1) {
    throw new SchemaValidationError("LevelInfo.title is too short");
  }
}

function validateLevelsResponse(data: ILevelsResponse): void {
  if (data.levels === undefined) {
    throw new SchemaValidationError("LevelsResponse.levels is undefined");
  }
  if (data.levels === null) {
    throw new SchemaValidationError("LevelsResponse.levels is null");
  }
  for (const fieldData of data.levels) {
    validateLevelInfo(fieldData);
  }
}

function validateLoginRequest(data: ILoginRequest): void {
  if (data.password === undefined) {
    throw new SchemaValidationError("LoginRequest.password is undefined");
  }
  if (data.password === null) {
    throw new SchemaValidationError("LoginRequest.password is null");
  }
  if (data.password.length < 1) {
    throw new SchemaValidationError("LoginRequest.password is too short");
  }
  if (data.username === undefined) {
    throw new SchemaValidationError("LoginRequest.username is undefined");
  }
  if (data.username === null) {
    throw new SchemaValidationError("LoginRequest.username is null");
  }
  if (data.username.length < 1) {
    throw new SchemaValidationError("LoginRequest.username is too short");
  }
}

function validateProfileInfoResponse(data: IProfileInfoResponse): void {
  if (data.auth_token === undefined) {
    throw new SchemaValidationError(
      "ProfileInfoResponse.auth_token is undefined",
    );
  }
  if (data.auth_token !== null) {
    if (data.auth_token.length < 1) {
      throw new SchemaValidationError(
        "ProfileInfoResponse.auth_token is too short",
      );
    }
  }
  if (data.authenticated === undefined) {
    throw new SchemaValidationError(
      "ProfileInfoResponse.authenticated is undefined",
    );
  }
  if (data.authenticated === null) {
    throw new SchemaValidationError(
      "ProfileInfoResponse.authenticated is null",
    );
  }
  if (data.email === undefined) {
    throw new SchemaValidationError("ProfileInfoResponse.email is undefined");
  }
  if (data.email !== null) {
    if (data.email.length < 1) {
      throw new SchemaValidationError("ProfileInfoResponse.email is too short");
    }
  }
  if (data.is_staff === undefined) {
    throw new SchemaValidationError(
      "ProfileInfoResponse.is_staff is undefined",
    );
  }
  if (data.is_staff === null) {
    throw new SchemaValidationError("ProfileInfoResponse.is_staff is null");
  }
  if (data.username === undefined) {
    throw new SchemaValidationError(
      "ProfileInfoResponse.username is undefined",
    );
  }
  if (data.username === null) {
    throw new SchemaValidationError("ProfileInfoResponse.username is null");
  }
  if (data.username.length < 1) {
    throw new SchemaValidationError(
      "ProfileInfoResponse.username is too short",
    );
  }
}

function validateQuotaResponse(data: IQuotaResponse): void {
  if (data.current === undefined) {
    throw new SchemaValidationError("QuotaResponse.current is undefined");
  }
  if (data.current === null) {
    throw new SchemaValidationError("QuotaResponse.current is null");
  }
  if (data.current < 0) {
    throw new SchemaValidationError(
      "QuotaResponse.current has a value below minimum",
    );
  }
  if (data.max === undefined) {
    throw new SchemaValidationError("QuotaResponse.max is undefined");
  }
  if (data.max === null) {
    throw new SchemaValidationError("QuotaResponse.max is null");
  }
  if (data.max < 0) {
    throw new SchemaValidationError(
      "QuotaResponse.max has a value below minimum",
    );
  }
}

function validateRegisterRequest(data: IRegisterRequest): void {
  if (data.email === undefined) {
    throw new SchemaValidationError("RegisterRequest.email is undefined");
  }
  if (data.email === null) {
    throw new SchemaValidationError("RegisterRequest.email is null");
  }
  if (data.email.length < 1) {
    throw new SchemaValidationError("RegisterRequest.email is too short");
  }
  if (data.password === undefined) {
    throw new SchemaValidationError("RegisterRequest.password is undefined");
  }
  if (data.password === null) {
    throw new SchemaValidationError("RegisterRequest.password is null");
  }
  if (data.password.length < 1) {
    throw new SchemaValidationError("RegisterRequest.password is too short");
  }
  if (data.username === undefined) {
    throw new SchemaValidationError("RegisterRequest.username is undefined");
  }
  if (data.username === null) {
    throw new SchemaValidationError("RegisterRequest.username is null");
  }
  if (data.username.length < 1) {
    throw new SchemaValidationError("RegisterRequest.username is too short");
  }
}

function validateServerInfoResponse(data: IServerInfoResponse): void {
  if (data.coop_url === undefined) {
    throw new SchemaValidationError("ServerInfoResponse.coop_url is undefined");
  }
  if (data.coop_url === null) {
    throw new SchemaValidationError("ServerInfoResponse.coop_url is null");
  }
  if (data.coop_url.length < 1) {
    throw new SchemaValidationError("ServerInfoResponse.coop_url is too short");
  }
  if (data.total_ghost_duration === undefined) {
    throw new SchemaValidationError(
      "ServerInfoResponse.total_ghost_duration is undefined",
    );
  }
  if (data.total_ghost_duration === null) {
    throw new SchemaValidationError(
      "ServerInfoResponse.total_ghost_duration is null",
    );
  }
  if (data.total_ghost_duration < 0) {
    throw new SchemaValidationError(
      "ServerInfoResponse.total_ghost_duration has a value below minimum",
    );
  }
  if (data.total_ghosts === undefined) {
    throw new SchemaValidationError(
      "ServerInfoResponse.total_ghosts is undefined",
    );
  }
  if (data.total_ghosts === null) {
    throw new SchemaValidationError("ServerInfoResponse.total_ghosts is null");
  }
  if (data.total_ghosts < 0) {
    throw new SchemaValidationError(
      "ServerInfoResponse.total_ghosts has a value below minimum",
    );
  }
  if (data.total_sessions === undefined) {
    throw new SchemaValidationError(
      "ServerInfoResponse.total_sessions is undefined",
    );
  }
  if (data.total_sessions === null) {
    throw new SchemaValidationError(
      "ServerInfoResponse.total_sessions is null",
    );
  }
  if (data.total_sessions < 0) {
    throw new SchemaValidationError(
      "ServerInfoResponse.total_sessions has a value below minimum",
    );
  }
  if (data.total_users === undefined) {
    throw new SchemaValidationError(
      "ServerInfoResponse.total_users is undefined",
    );
  }
  if (data.total_users === null) {
    throw new SchemaValidationError("ServerInfoResponse.total_users is null");
  }
  if (data.total_users < 0) {
    throw new SchemaValidationError(
      "ServerInfoResponse.total_users has a value below minimum",
    );
  }
}

function validateSession(data: ISession): void {
  if (data.description === undefined) {
    throw new SchemaValidationError("Session.description is undefined");
  }
  if (data.description === null) {
    throw new SchemaValidationError("Session.description is null");
  }
  if (data.id === undefined) {
    throw new SchemaValidationError("Session.id is undefined");
  }
  if (data.id === null) {
    throw new SchemaValidationError("Session.id is null");
  }
  if (data.id.length < 1) {
    throw new SchemaValidationError("Session.id is too short");
  }
  if (data.owner === undefined) {
    throw new SchemaValidationError("Session.owner is undefined");
  }
  if (data.owner === null) {
    throw new SchemaValidationError("Session.owner is null");
  }
  if (data.owner.length < 1) {
    throw new SchemaValidationError("Session.owner is too short");
  }
  if (data.players === undefined) {
    throw new SchemaValidationError("Session.players is undefined");
  }
  if (data.players === null) {
    throw new SchemaValidationError("Session.players is null");
  }
  for (const fieldData of data.players) {
    if (fieldData === undefined) {
      throw new SchemaValidationError("Session.players is undefined");
    }
    if (fieldData === null) {
      throw new SchemaValidationError("Session.players is null");
    }
    if (fieldData.length < 1) {
      throw new SchemaValidationError("Session.players is too short");
    }
  }

  if (data.private === undefined) {
    throw new SchemaValidationError("Session.private is undefined");
  }
  if (data.private === null) {
    throw new SchemaValidationError("Session.private is null");
  }
  if (data.tags === undefined) {
    throw new SchemaValidationError("Session.tags is undefined");
  }
  if (data.tags === null) {
    throw new SchemaValidationError("Session.tags is null");
  }
  for (const fieldData of data.tags) {
    validateTag(fieldData);
  }

  if (data.time === undefined) {
    throw new SchemaValidationError("Session.time is undefined");
  }
  if (data.time !== null) {
    validateTimeSpan(data.time);
  }
}

function validateSessionAccessRequest(data: ISessionAccessRequest): void {
  if (data.api_key === undefined) {
    throw new SchemaValidationError(
      "SessionAccessRequest.api_key is undefined",
    );
  }
  if (data.api_key === null) {
    throw new SchemaValidationError("SessionAccessRequest.api_key is null");
  }
  if (data.api_key.length < 1) {
    throw new SchemaValidationError(
      "SessionAccessRequest.api_key is too short",
    );
  }
  if (data.auth_token === undefined) {
    throw new SchemaValidationError(
      "SessionAccessRequest.auth_token is undefined",
    );
  }
  if (data.auth_token === null) {
    throw new SchemaValidationError("SessionAccessRequest.auth_token is null");
  }
  if (data.auth_token.length < 1) {
    throw new SchemaValidationError(
      "SessionAccessRequest.auth_token is too short",
    );
  }
  if (data.session_id === undefined) {
    throw new SchemaValidationError(
      "SessionAccessRequest.session_id is undefined",
    );
  }
  if (data.session_id === null) {
    throw new SchemaValidationError("SessionAccessRequest.session_id is null");
  }
  if (data.session_id.length < 1) {
    throw new SchemaValidationError(
      "SessionAccessRequest.session_id is too short",
    );
  }
  if (data.username === undefined) {
    throw new SchemaValidationError(
      "SessionAccessRequest.username is undefined",
    );
  }
  if (data.username === null) {
    throw new SchemaValidationError("SessionAccessRequest.username is null");
  }
  if (data.username.length < 1) {
    throw new SchemaValidationError(
      "SessionAccessRequest.username is too short",
    );
  }
}

function validateSessionPlayers(data: ISessionPlayers): void {
  if (data.session_id === undefined) {
    throw new SchemaValidationError("SessionPlayers.session_id is undefined");
  }
  if (data.session_id === null) {
    throw new SchemaValidationError("SessionPlayers.session_id is null");
  }
  if (data.session_id.length < 1) {
    throw new SchemaValidationError("SessionPlayers.session_id is too short");
  }
  if (data.usernames === undefined) {
    throw new SchemaValidationError("SessionPlayers.usernames is undefined");
  }
  if (data.usernames === null) {
    throw new SchemaValidationError("SessionPlayers.usernames is null");
  }
  for (const fieldData of data.usernames) {
    if (fieldData === undefined) {
      throw new SchemaValidationError("SessionPlayers.usernames is undefined");
    }
    if (fieldData === null) {
      throw new SchemaValidationError("SessionPlayers.usernames is null");
    }
    if (fieldData.length < 1) {
      throw new SchemaValidationError("SessionPlayers.usernames is too short");
    }
  }
}

function validateSessionResponse(data: ISessionResponse): void {
  if (data.session === undefined) {
    throw new SchemaValidationError("SessionResponse.session is undefined");
  }
  if (data.session !== null) {
    validateSession(data.session);
  }
}

function validateSessionsPlayersRequest(data: ISessionsPlayersRequest): void {
  if (data.api_key === undefined) {
    throw new SchemaValidationError(
      "SessionsPlayersRequest.api_key is undefined",
    );
  }
  if (data.api_key === null) {
    throw new SchemaValidationError("SessionsPlayersRequest.api_key is null");
  }
  if (data.api_key.length < 1) {
    throw new SchemaValidationError(
      "SessionsPlayersRequest.api_key is too short",
    );
  }
  if (data.sessions === undefined) {
    throw new SchemaValidationError(
      "SessionsPlayersRequest.sessions is undefined",
    );
  }
  if (data.sessions === null) {
    throw new SchemaValidationError("SessionsPlayersRequest.sessions is null");
  }
  for (const fieldData of data.sessions) {
    validateSessionPlayers(fieldData);
  }
}

function validateSessionsResponse(data: ISessionsResponse): void {
  if (data.sessions === undefined) {
    throw new SchemaValidationError("SessionsResponse.sessions is undefined");
  }
  if (data.sessions === null) {
    throw new SchemaValidationError("SessionsResponse.sessions is null");
  }
  for (const fieldData of data.sessions) {
    validateSession(fieldData);
  }
}

function validateSuccessResponse(data: ISuccessResponse): void {
  if (data.message === undefined) {
    throw new SchemaValidationError("SuccessResponse.message is undefined");
  }
  if (data.message === null) {
    throw new SchemaValidationError("SuccessResponse.message is null");
  }
  if (data.success === undefined) {
    throw new SchemaValidationError("SuccessResponse.success is undefined");
  }
  if (data.success === null) {
    throw new SchemaValidationError("SuccessResponse.success is null");
  }
}

function validateTag(data: ITag): void {
  if (data.description === undefined) {
    throw new SchemaValidationError("Tag.description is undefined");
  }
  if (data.description === null) {
    throw new SchemaValidationError("Tag.description is null");
  }
  if (data.id === undefined) {
    throw new SchemaValidationError("Tag.id is undefined");
  }
  if (data.id === null) {
    throw new SchemaValidationError("Tag.id is null");
  }
  if (data.name === undefined) {
    throw new SchemaValidationError("Tag.name is undefined");
  }
  if (data.name === null) {
    throw new SchemaValidationError("Tag.name is null");
  }
  if (data.name.length < 1) {
    throw new SchemaValidationError("Tag.name is too short");
  }
}

function validateTagsResponse(data: ITagsResponse): void {
  if (data.tags === undefined) {
    throw new SchemaValidationError("TagsResponse.tags is undefined");
  }
  if (data.tags === null) {
    throw new SchemaValidationError("TagsResponse.tags is null");
  }
  for (const fieldData of data.tags) {
    validateTag(fieldData);
  }
}

function validateTimeSpan(data: ITimeSpan): void {
  if (data.end === undefined) {
    throw new SchemaValidationError("TimeSpan.end is undefined");
  }
  if (data.end === null) {
    throw new SchemaValidationError("TimeSpan.end is null");
  }
  if (
    !data.end.match(
      /^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?(\+[0-9]{2}:[0-9]{2}|Z)$/,
    )
  ) {
    throw new SchemaValidationError("TimeSpan.end has an invalid format");
  }
  if (data.start === undefined) {
    throw new SchemaValidationError("TimeSpan.start is undefined");
  }
  if (data.start === null) {
    throw new SchemaValidationError("TimeSpan.start is null");
  }
  if (
    !data.start.match(
      /^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?(\+[0-9]{2}:[0-9]{2}|Z)$/,
    )
  ) {
    throw new SchemaValidationError("TimeSpan.start has an invalid format");
  }
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
  body: ICreateSessionRequest,
): Promise<ISuccessResponse> {
  validateCreateSessionRequest(body);
  const result = (await doPost(`/api/v0/sessions`, body)) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}

export async function getSession(sessionId: string): Promise<ISessionResponse> {
  const result = (await doGet(
    `/api/v0/sessions/${encodeURIComponent(sessionId)}`,
  )) as ISessionResponse;
  validateSessionResponse(result);
  return result;
}

export async function editSession(
  sessionId: string,
  body: ICreateSessionRequest,
): Promise<ISuccessResponse> {
  validateCreateSessionRequest(body);
  const result = (await doPost(
    `/api/v0/sessions/${encodeURIComponent(sessionId)}`,
    body,
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}

export async function deleteSession(
  sessionId: string,
): Promise<ISuccessResponse> {
  const result = (await doDelete(
    `/api/v0/sessions/${encodeURIComponent(sessionId)}`,
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}

export async function checkSessionAccess(
  body: ISessionAccessRequest,
): Promise<ISuccessResponse> {
  validateSessionAccessRequest(body);
  const result = (await doPost(
    `/api/v0/sessions/check-access`,
    body,
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}

export async function updateSessionsPlayers(
  body: ISessionsPlayersRequest,
): Promise<IEmpty> {
  validateSessionsPlayersRequest(body);
  const result = (await doPost(
    `/api/v0/sessions/session-players`,
    body,
  )) as IEmpty;
  validateEmpty(result);
  return result;
}

export async function getAnnouncements(): Promise<IAnnouncementsResponse> {
  const result = (await doGet(
    `/api/v0/announcements`,
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
  body: IChangeUsernameRequest,
): Promise<ISuccessResponse> {
  validateChangeUsernameRequest(body);
  const result = (await doPost(
    `/api/v0/auth/change-username`,
    body,
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
  body: IRegisterRequest,
): Promise<ISuccessResponse> {
  validateRegisterRequest(body);
  const result = (await doPost(
    `/api/v0/auth/register`,
    body,
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}

export async function changePassword(
  body: IChangePasswordRequest,
): Promise<ISuccessResponse> {
  validateChangePasswordRequest(body);
  const result = (await doPost(
    `/api/v0/auth/change-password`,
    body,
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}

export async function changeEmail(
  body: IChangeEmailRequest,
): Promise<ISuccessResponse> {
  validateChangeEmailRequest(body);
  const result = (await doPost(
    `/api/v0/auth/change-email`,
    body,
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}

export async function logout(): Promise<IEmpty> {
  const result = (await doGet(`/api/v0/auth/logout`)) as IEmpty;
  validateEmpty(result);
  return result;
}

export async function getGhosts(): Promise<IGhostFilesResponse> {
  const result = (await doGet(`/api/v0/ghosts`)) as IGhostFilesResponse;
  validateGhostFilesResponse(result);
  return result;
}

export async function uploadGhost(files: File[]): Promise<ISuccessResponse> {
  const result = (await doPostFiles(
    `/api/v0/ghosts`,
    files,
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}

export async function downloadGhost(
  id: number,
): Promise<ReadableStream<Uint8Array> | null> {
  const result = (await doGetFile(
    `/api/v0/ghosts/${encodeURIComponent(id)}/download`,
  )) as ReadableStream<Uint8Array> | null;
  return result;
}

export async function getGhost(id: number): Promise<IGhostFileResponse> {
  const result = (await doGet(
    `/api/v0/ghosts/${encodeURIComponent(id)}`,
  )) as IGhostFileResponse;
  validateGhostFileResponse(result);
  return result;
}

export async function updateGhost(
  id: number,
  body: IGhostInfoRequest,
): Promise<ISuccessResponse> {
  validateGhostInfoRequest(body);
  const result = (await doPost(
    `/api/v0/ghosts/${encodeURIComponent(id)}`,
    body,
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}

export async function deleteGhost(id: number): Promise<ISuccessResponse> {
  const result = (await doDelete(
    `/api/v0/ghosts/${encodeURIComponent(id)}`,
  )) as ISuccessResponse;
  validateSuccessResponse(result);
  return result;
}

export async function getStagingGhosts(): Promise<IGhostFilesResponse> {
  const result = (await doGet(`/api/v0/ghosts/staging`)) as IGhostFilesResponse;
  validateGhostFilesResponse(result);
  return result;
}

export async function getGhostsQuota(): Promise<IQuotaResponse> {
  const result = (await doGet(`/api/v0/ghosts/quota`)) as IQuotaResponse;
  validateQuotaResponse(result);
  return result;
}

export async function getAlternativeLevels(
  identifier: string,
): Promise<ILevelsResponse> {
  const result = (await doGet(
    `/api/v0/levels/${encodeURIComponent(identifier)}`,
  )) as ILevelsResponse;
  validateLevelsResponse(result);
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
  if (csrftoken != null) {
    headers.append("X-CSRFToken", csrftoken);
  }
  return headers;
}

export async function doGet(url: string): Promise<object> {
  return await fetch(`${env.VITE_APP_SERVER_URL}${url}`, {
    credentials: "include",
    headers: getCsrfHeader(),
  }).then((r) => r.json());
}

export async function doGetFile(
  url: string,
): Promise<ReadableStream<Uint8Array> | null> {
  return await fetch(`${env.VITE_APP_SERVER_URL}${url}`, {
    credentials: "include",
    headers: getCsrfHeader(),
  }).then((r) => r.body);
}

export async function doDelete(url: string): Promise<object> {
  return await fetch(`${env.VITE_APP_SERVER_URL}${url}`, {
    method: "DELETE",
    credentials: "include",
    headers: getCsrfHeader(),
  }).then((r) => r.json());
}

export async function doPost(url: string, body: object): Promise<object> {
  return await fetch(`${env.VITE_APP_SERVER_URL}${url}`, {
    method: "POST",
    credentials: "include",
    headers: getCsrfHeader(),
    body: JSON.stringify(body),
  }).then((r) => r.json());
}

export async function doPostFiles(url: string, files: File[]): Promise<object> {
  const formData = new FormData();
  for (const file of files) {
    formData.append(file.name, file);
  }
  return await fetch(`${env.VITE_APP_SERVER_URL}${url}`, {
    method: "POST",
    credentials: "include",
    headers: getCsrfHeader(),
    body: formData,
  }).then((r) => r.json());
}

export class SchemaValidationError implements Error {
  public constructor(public readonly message: string) {
    this.name = "SchemaValidationError";
  }

  name: string;
}
