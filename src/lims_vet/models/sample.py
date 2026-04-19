from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, JSON, DateTime, Enum, Text
from sqlalchemy.sql import func
import enum
from datetime import datetime
from .base import Base, UUIDMixin

class SampleStatus(str, enum.Enum):
    RECEIVED = "received"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"

class Sample(Base, UUIDMixin):
    __tablename__ = "samples"

    patient_name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_name: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[SampleStatus] = mapped_column(Enum(SampleStatus), nullable=False, default=SampleStatus.RECEIVED)
    
    # Store the extracted results as JSON
    results_data: Mapped[dict] = mapped_column(JSON, nullable=True)
    
    # Raw text or file reference if needed
    raw_text: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)