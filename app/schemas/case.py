from datetime import datetime
from pydantic import BaseModel, Field

from app.models.case import CasePriority, CaseStatus
from app.schemas.user import UserRead


class CaseCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    patient_code: str | None = Field(default=None, max_length=64)
    description: str = Field(min_length=10)
    priority: CasePriority = CasePriority.medium


class CaseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=255)
    patient_code: str | None = Field(default=None, max_length=64)
    description: str | None = Field(default=None, min_length=10)
    status: CaseStatus | None = None
    priority: CasePriority | None = None


class CaseRead(BaseModel):
    id: int
    title: str
    patient_code: str | None
    description: str
    status: CaseStatus
    priority: CasePriority
    created_by: UserRead
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class StatusHistoryRead(BaseModel):
    id: int
    old_status: CaseStatus | None
    new_status: CaseStatus
    changed_by_id: int
    changed_at: datetime

    model_config = {"from_attributes": True}
