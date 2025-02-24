from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    id: int = Field(None, description="ID")
    permissions: list[str] = Field(None, description="Permissions")

    class Config:
        validate_assignment = True
