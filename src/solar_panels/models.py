import enum

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, func, Enum
)
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from src.core.db.session import Base


class PanelStatus(enum.Enum):
    OPERATIONAL = "OPERATIONAL"
    MAINTENANCE = "MAINTENANCE"
    OFFLINE = "OFFLINE"
    UNKNOWN = "UNKNOWN"


class SolarPanel(Base):
    __tablename__ = 'solar_panels'

    # Identification and Metadata
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
    orientation = Column(Float, nullable=True)  # degrees from North
    tilt = Column(Float, nullable=True)  # Tilt angle in degrees

    # Operational Data
    status = Column(Enum(PanelStatus), nullable=True)  # "operational", "maintenance", "offline"

    # Geolocation Data
    location = Column(Geometry('POINT', srid=4326), nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship("User", back_populates="solar_panels")

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"""<SolarPanel(
            id={self.id}, serial_number="{self.serial_number}", name="{self.name}",
            manufacturer="{self.manufacturer}", model="{self.model}", installation_date="{self.installation_date.isoformat() if self.installation_date else None}",
            capacity_kw={self.capacity_kw}, efficiency={self.efficiency}, voltage_rating={self.voltage_rating},
            current_rating={self.current_rating}, width={self.width}, length={self.length}, height={self.height},
            weight={self.weight}, orientation={self.orientation}, tilt={self.tilt}, 
            status="{self.status.name}", 
            location="{self.location}", 
            user_id={self.user_id}, created_at="{self.created_at.isoformat() if self.created_at else None}", 
            updated_at="{self.updated_at.isoformat() if self.updated_at else None}"
        )>"""
