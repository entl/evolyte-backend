from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, Field, model_validator


class UserBase(BaseModel):
    """
    Represents the base model for user information.

    Attributes:
        username (str): The username of the user.
        full_name (str): The full name of the user.

    """

    full_name: Annotated[
        str,
        Field(min_length=1, max_length=128, description="The full name of the user"),
    ]


class UserCreate(UserBase):
    """
    Represents the input model for creating a new user.

    Attributes:
        email (EmailStr): The email of the user.
        password (str): The password of the user.
    """

    email: Annotated[EmailStr, Field(..., description="The email of the user")]
    password: Annotated[str, Field(..., min_length=8, max_length=128)]
    password_confirmation: Annotated[str, Field(..., min_length=8, max_length=128)]

    @model_validator(mode="after")
    def check_password_confirmation(cls, m):
        if m.password != m.password_confirmation:
            raise ValueError("Password and password confirmation do not match")

        return m


class UserResponse(UserBase):
    """
    Represents the output model for user information.

    Attributes:
        id (int): The unique identifier of the user.
        email (EmailStr): The email of the user.
    """

    id: Annotated[int, Field(..., description="The unique identifier of the user")]
    email: Annotated[EmailStr, Field(..., description="The email of the user")]

    created_at: Annotated[datetime, Field(..., description="The datetime of the user's creation")]
    updated_at: Annotated[datetime, Field(..., description="The datetime of the user's last update")]

    class Config:
        from_attributes = True
        populate_by_name = True


class UserUpdate(BaseModel):
    id: Annotated[int, Field(..., description="The unique identifier of the user")]
    email: Optional[EmailStr] = Field(default=None, description="The email of the user")

    full_name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=128,
        description="The full name of the user",
    )
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)
