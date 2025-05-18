import enum

from sqlalchemy import Column, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import relationship

from src.core.db.session import Base


class Roles(enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    password = Column(String, nullable=True)

    role = Column(Enum(Roles), nullable=False, default=Roles.USER)

    # Relationships
    solar_panels = relationship("SolarPanel", back_populates="user")
    identities = relationship("Identity", back_populates="user")

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
