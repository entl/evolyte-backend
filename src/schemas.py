from pydantic import BaseModel, Field

from src.user.schemas import UserRoles


class CurrentUser(BaseModel):
    id: int = Field(None, description="ID")
    role: str = Field(None, description="User role")
    permissions: list[str] = Field(None, description="Permissions")

    class Config:
        validate_assignment = True
