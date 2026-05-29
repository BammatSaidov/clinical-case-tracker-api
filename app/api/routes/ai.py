from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.ai_summary import AISummary
from app.models.case import ClinicalCase
from app.models.checklist import ChecklistItem
from app.models.comment import Comment
from app.models.user import User
from app.schemas.ai import AISummaryRead
from app.services.ai.provider import get_ai_provider

router = APIRouter(prefix="/cases/{case_id}/ai", tags=["ai"])


@router.post("/summary", response_model=AISummaryRead, status_code=status.HTTP_201_CREATED)
def generate_ai_summary(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AISummary:
    case = db.get(ClinicalCase, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    comments = list(db.scalars(select(Comment).where(Comment.case_id == case_id).order_by(Comment.created_at)).all())
    checklist_items = list(db.scalars(select(ChecklistItem).where(ChecklistItem.case_id == case_id).order_by(ChecklistItem.created_at)).all())

    provider = get_ai_provider()
    summary_text = provider.generate_case_summary(case=case, comments=comments, checklist_items=checklist_items)
    summary = AISummary(case_id=case_id, provider=provider.name, summary=summary_text)

    db.add(summary)
    db.commit()
    db.refresh(summary)
    return summary


@router.get("/summaries", response_model=list[AISummaryRead])
def list_ai_summaries(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[AISummary]:
    if not db.get(ClinicalCase, case_id):
        raise HTTPException(status_code=404, detail="Case not found")

    return list(db.scalars(select(AISummary).where(AISummary.case_id == case_id).order_by(AISummary.created_at.desc())).all())
