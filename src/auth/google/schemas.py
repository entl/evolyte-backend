from typing import Optional

from pydantic import BaseModel, Field


class GoogleOAuth2TokenResponse(BaseModel):
    access_token: str
    expires_in: int
    token_type: str
    id_token: str
    scope: str


class GoogleUserInfoResponse(BaseModel):
    sub: str
    name: str
    given_name: str
    family_name: Optional[str] = Field(default=None)
    picture: str
    email: str
    email_verified: bool


class GoogleOAuth2Response(BaseModel):
    user: GoogleUserInfoResponse
    tokens: GoogleOAuth2TokenResponse


class GoogleUserInfoErrorResponse(BaseModel):
    error: str
    error_description: str
    error_uri: str


class GoogleOAuth2TokenErrorResponse(BaseModel):
    error: str
    error_description: str
    error_uri: str