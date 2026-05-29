from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.user import UserRead


class CommentCreate(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class CommentRead(BaseModel):
    id: int
    case_id: int
    text: str
    author: UserRead
    created_at: datetime

    model_config = {"from_attributes": True}
