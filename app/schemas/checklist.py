from datetime import datetime
from pydantic import BaseModel, Field


class ChecklistItemCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)


class ChecklistItemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=255)
    is_done: bool | None = None


class ChecklistItemRead(BaseModel):
    id: int
    case_id: int
    title: str
    is_done: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
