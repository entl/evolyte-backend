from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from src.core.db.session import Base


class Identity(Base):
    __tablename__ = "identities"
    __table_args__ = (
        UniqueConstraint("user_id", "provider", name="uq_user_provider"),
        UniqueConstraint("provider", "provider_user_id", name="uq_user_provider_user_id"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = Column(String, nullable=False)
    provider_user_id = Column(String, nullable=False)

    access_token = Column(String, nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="identities")

    def __repr__(self):
        return f"<Identity(id={self.id}, user_id={self.user_id}, provider={self.provider}, provider_user_id={self.provider_user_id})>"
