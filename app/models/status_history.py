from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.case import CaseStatus


class StatusHistory(Base):
    __tablename__ = "status_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("clinical_cases.id"), nullable=False, index=True)
    old_status: Mapped[CaseStatus | None] = mapped_column(Enum(CaseStatus), nullable=True)
    new_status: Mapped[CaseStatus] = mapped_column(Enum(CaseStatus), nullable=False)
    changed_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    case = relationship("ClinicalCase", back_populates="status_history")
