from src.core.db.session import Base
from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship


class Inverter(Base):
    __tablename__ = "inverters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    vendor = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    serial_number = Column(String(100), unique=True, nullable=False)
    total_lifetime_production_kwh = Column(Float, nullable=False, default=0.0)
    installation_date = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False)

    hourly_records = relationship("SolarPanelHourlyRecord", back_populates="inverter")
    solar_panels = relationship("SolarPanel", back_populates="inverter")
    

    def __repr__(self):
        return f"<Inverter(id={self.id}, user_id={self.user_id}, vendor={self.vendor}, model={self.model}, serial_number={self.serial_number}, installation_date={self.installation_date})>"