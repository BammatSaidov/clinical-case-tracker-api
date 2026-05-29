from datetime import datetime
from pydantic import BaseModel


class AISummaryRead(BaseModel):
    id: int
    case_id: int
    provider: str
    summary: str
    created_at: datetime

    model_config = {"from_attributes": True}
