from typing import Literal, Optional

from pydantic import BaseModel, Field


# Token schemas
class TokenPayload(BaseModel):
    user_id: int = Field(..., description="User ID")
    sub: Literal["access", "refresh"] = Field(..., description="Token type")
    exp: int = Field(..., description="Expiration time of the token")


class TokenPair(BaseModel):
    access_token: str = Field(..., description="Access token")
    refresh_token: str = Field(..., description="Refresh token")
    token_type: str = Field(default="bearer", description="Type of token")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="Token")
    token_type: str = Field(default="bearer", description="Type of token")


class VerifyTokenRequest(BaseModel):
    access_token: str = Field(..., description="Token")
