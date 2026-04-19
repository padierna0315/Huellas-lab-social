from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, UUIDMixin

class Message(Base, UUIDMixin):
    __tablename__ = "messages"

    topic: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    
    sender_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())