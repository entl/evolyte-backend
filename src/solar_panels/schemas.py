from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class PanelStatusEnum(str, Enum):
    OPERATIONAL = "OPERATIONAL"
    MAINTENANCE = "MAINTENANCE"
    OFFLINE = "OFFLINE"
    UNKNOWN = "UNKNOWN"


class SolarPanelBase(BaseModel):
    serial_number: str = Field(..., example="SP-123456")
    name: str = Field(..., example="Main Roof Panel")
    manufacturer: Optional[str] = Field(None, example="SolarTech Inc.")
    model: Optional[str] = Field(None, example="ST-500")
    installation_date: Optional[datetime] = Field(None, example="2024-01-01T12:00:00")

    capacity_kw: float = Field(..., example=5.0)
    efficiency: Optional[float] = Field(None, example=18.5)
    voltage_rating: Optional[float] = Field(None, example=48.0)
    current_rating: Optional[float] = Field(None, example=10.0)
    width: Optional[float] = Field(None, example=1.2)
    length: Optional[float] = Field(None, example=2.0)
    height: Optional[float] = Field(None, example=0.05)
    weight: Optional[float] = Field(None, example=25.0)
    orientation: Optional[float] = Field(None, example=180.0)  # Degrees from North
    tilt: Optional[float] = Field(None, example=30.0)

    status: Optional[PanelStatusEnum] = Field(None, example="operational")

    location: tuple[float, float] = Field(..., example=(51.5074, -0.1278))  # Latitude & Longitude


class SolarPanelCreate(SolarPanelBase):
    user_id: Optional[int] = Field(None, example=1)  # user id is None for solar panels from open data sources


class SolarPanelUpdate(SolarPanelBase):
    pass


class SolarPanelResponse(SolarPanelBase):
    id: int
    user_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
