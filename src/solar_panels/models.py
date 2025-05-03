import enum

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func, Enum
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from src.core.db.session import Base


class PanelStatus(enum.Enum):
    OPERATIONAL = "OPERATIONAL"
    MAINTENANCE = "MAINTENANCE"
    OFFLINE = "OFFLINE"
    UNKNOWN = "UNKNOWN"


class SolarPanelHourlyRecord(Base):
    __tablename__ = "solar_panel_hourly_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    solar_panel_id = Column(Integer, ForeignKey("solar_panels.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)

    # Power Production Data
    power_output_kw = Column(Float, nullable=False)  # instant kw
    energy_generated_kwh = Column(Float, nullable=False)  # cumulative kwh
    predicted_power_output_kw = Column(Float, nullable=True)  # predicted kwh

    # Performance Metrics
    efficiency_percent = Column(Float, nullable=True)  # Actual efficiency

    # Environmental Conditions
    cell_temperature_celsius = Column(Float, nullable=True)  # cell temperature
    temperature_celsius = Column(Float, nullable=True)  # Ambient temperature
    irradiance = Column(Float, nullable=True)  # Solar irradiance
    poa_irradiance = Column(Float, nullable=True)  # Plane of array irradiance
    cloud_cover_percent = Column(Float, nullable=True)
    wind_speed_kmh = Column(Float, nullable=True)
    wind_direction_degrees = Column(Float, nullable=True)
    humidity_percent = Column(Float, nullable=True)
    precipitation_mm = Column(Float, nullable=True)
    pressure_msl_hpa = Column(Float, nullable=True)
    clear_sky_index = Column(Float, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    solar_panel = relationship("SolarPanel", back_populates="hourly_records")

    def __repr__(self):
        return f"<SolarPanelHourlyRecord(id={self.id}, panel_id={self.solar_panel_id}, timestamp={self.timestamp}, power_output={self.power_output_kw}kW)>"


class SolarPanel(Base):
    __tablename__ = "solar_panels"

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
    status = Column(
        Enum(PanelStatus), nullable=True
    )  # "operational", "maintenance", "offline"

    # Geolocation Data
    location = Column(Geometry("POINT", srid=4326), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="solar_panels")

    hourly_records = relationship(
        "SolarPanelHourlyRecord", back_populates="solar_panel"
    )

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
