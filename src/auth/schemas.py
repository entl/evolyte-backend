from typing import Literal, Optional

from pydantic import BaseModel, Field


# Token schemas
class TokenPayload(BaseModel):
    user_id: int = Field(..., description="User ID")
    sub: Literal["access", "refresh"] = Field(..., description="Token type")
    exp: int = Field(..., description="Expiration time of the token")


class TokenPairResponse(BaseModel):
    access_token: str = Field(..., description="Token")
    refresh_token: Optional[str] = Field(..., description="Token")
    token_type: str = Field(default="bearer", description="Type of token")


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="Token")


class VerifyTokenRequest(BaseModel):
    access_token: str = Field(..., description="Token")
