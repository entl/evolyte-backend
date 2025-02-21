import enum

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, func, Enum
)
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from src.core.db.session import Base


class PanelStatus(enum.Enum):
    OPERATIONAL = "operational"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"
    UNKNOWN = "unknown"


class SolarPanel(Base):
    __tablename__ = 'solar_panels'

    # Identification & Metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    serial_number = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    manufacturer = Column(String, nullable=True)
    model = Column(String, nullable=True)
    installation_date = Column(DateTime, default=func.now())

    # Technical Specifications
    capacity_kw = Column(Float, nullable=False)  # Maximum power output in kW
    efficiency = Column(Float, nullable=True)  # Conversion efficiency (%)
    voltage_rating = Column(Float, nullable=True)  # Voltage rating (V)
    current_rating = Column(Float, nullable=True)  # Current rating (A)
    width = Column(Float, nullable=True)  # Width in meters
    length = Column(Float, nullable=True)  # Length in meters
    height = Column(Float, nullable=True)  # Height in meters
    weight = Column(Float, nullable=True)  # Weight in kilograms
    orientation = Column(Float, nullable=True)  # e.g., degrees from North
    tilt = Column(Float, nullable=True)  # Tilt angle in degrees

    # Operational Data
    status = Column(Enum(PanelStatus), nullable=True)  # e.g., "operational", "maintenance", "offline"

    # Geolocation Data
    location = Column(Geometry('POINT', srid=4326), nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship("User", back_populates="solar_panels")

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return (f"<SolarPanel(id={self.id}, serial_number={self.serial_number}, "
                f"manufacturer={self.manufacturer}, model={self.model}, "
                f"kwp={self.capacity_kw})>")
