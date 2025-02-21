from datetime import datetime, date
from typing import Optional, Annotated

from pydantic import EmailStr, Field, BaseModel


class UserBase(BaseModel):
    """
    Represents the base model for user information.

    Attributes:
        username (str): The username of the user.
        full_name (str): The full name of the user.

    """
    username: Annotated[str, Field(pattern="^[A-Za-z0-9-_.]+$", to_lower=True,
                                   strip_whitespace=True, description="The username of the user",
                                   min_length=4, max_length=128)]
    full_name: Annotated[str, Field(min_length=1, max_length=128, description="The full name of the user")]

    created_at: Annotated[datetime, Field(..., description="The datetime of the user's creation")]
    updated_at: Annotated[datetime, Field(..., description="The datetime of the user's last update")]


class UserCreate(UserBase):
    """
    Represents the input model for creating a new user.

    Attributes:
        email (EmailStr): The email of the user.
        password (str): The password of the user.
    """
    email: Annotated[EmailStr, Field(..., description="The email of the user")]
    password: Annotated[str, Field(..., min_length=8, max_length=128)]


class UserOut(UserBase):
    """
    Represents the output model for user information.

    Attributes:
        id (int): The unique identifier of the user.
        email (EmailStr): The email of the user.
    """
    id: Annotated[int, Field(..., description="The unique identifier of the user")]
    email: Annotated[EmailStr, Field(..., description="The email of the user")]

    class Config:
        from_attributes = True
        populate_by_name = True


class UserUpdate(BaseModel):
    id: Annotated[int, Field(..., description="The unique identifier of the user")]
    email: Optional[EmailStr] = Field(default=None, description="The email of the user")
    username: Optional[str] = Field(default=None, pattern="^[A-Za-z0-9-_.]+$", to_lower=True, strip_whitespace=True,
                                    description="The username of the user", min_length=4, max_length=128)
    full_name: Optional[str] = Field(default=None, min_length=1, max_length=128, description="The full name of the user")
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)


class LoginResponse(BaseModel):
    access_token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
    token_type: str = Field(..., description="Type of token")
