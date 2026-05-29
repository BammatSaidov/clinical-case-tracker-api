from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.case import ClinicalCase
from app.models.checklist import ChecklistItem
from app.models.user import User
from app.schemas.checklist import ChecklistItemCreate, ChecklistItemRead, ChecklistItemUpdate

router = APIRouter(prefix="/cases/{case_id}/checklist", tags=["checklist"])


@router.post("", response_model=ChecklistItemRead, status_code=status.HTTP_201_CREATED)
def create_checklist_item(
    case_id: int,
    payload: ChecklistItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChecklistItem:
    if not db.get(ClinicalCase, case_id):
        raise HTTPException(status_code=404, detail="Case not found")

    item = ChecklistItem(case_id=case_id, title=payload.title)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("", response_model=list[ChecklistItemRead])
def list_checklist_items(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ChecklistItem]:
    if not db.get(ClinicalCase, case_id):
        raise HTTPException(status_code=404, detail="Case not found")

    return list(
        db.scalars(
            select(ChecklistItem)
            .where(ChecklistItem.case_id == case_id)
            .order_by(ChecklistItem.created_at)
        ).all()
    )


@router.patch("/{item_id}", response_model=ChecklistItemRead)
def update_checklist_item(
    case_id: int,
    item_id: int,
    payload: ChecklistItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChecklistItem:
    item = db.scalar(
        select(ChecklistItem).where(
            ChecklistItem.id == item_id,
            ChecklistItem.case_id == case_id,
        )
    )
    if not item:
        raise HTTPException(status_code=404, detail="Checklist item not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item
