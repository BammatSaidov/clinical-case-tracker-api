import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CaseStatus(str, enum.Enum):
    new = "new"
    in_progress = "in_progress"
    needs_review = "needs_review"
    done = "done"
    rejected = "rejected"


class CasePriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ClinicalCase(Base):
    __tablename__ = "clinical_cases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    patient_code: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[CaseStatus] = mapped_column(Enum(CaseStatus), default=CaseStatus.new, nullable=False, index=True)
    priority: Mapped[CasePriority] = mapped_column(Enum(CasePriority), default=CasePriority.medium, nullable=False)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    created_by = relationship("User", back_populates="cases")
    comments = relationship("Comment", back_populates="case", cascade="all, delete-orphan")
    checklist_items = relationship("ChecklistItem", back_populates="case", cascade="all, delete-orphan")
    status_history = relationship("StatusHistory", back_populates="case", cascade="all, delete-orphan")
    ai_summaries = relationship("AISummary", back_populates="case", cascade="all, delete-orphan")
