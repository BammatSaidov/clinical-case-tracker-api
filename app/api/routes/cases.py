from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.case import CaseStatus, ClinicalCase
from app.models.status_history import StatusHistory
from app.models.user import User
from app.schemas.case import CaseCreate, CaseRead, CaseUpdate, StatusHistoryRead

router = APIRouter(prefix="/cases", tags=["cases"])


@router.post("", response_model=CaseRead, status_code=status.HTTP_201_CREATED)
def create_case(
    payload: CaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ClinicalCase:
    case = ClinicalCase(**payload.model_dump(), created_by_id=current_user.id)
    db.add(case)
    db.flush()
    db.add(StatusHistory(case_id=case.id, old_status=None, new_status=case.status, changed_by_id=current_user.id))
    db.commit()
    db.refresh(case)
    return db.scalar(
        select(ClinicalCase)
        .options(selectinload(ClinicalCase.created_by))
        .where(ClinicalCase.id == case.id)
    )


@router.get("", response_model=list[CaseRead])
def list_cases(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    status_filter: CaseStatus | None = Query(default=None, alias="status"),
    search: str | None = Query(default=None, min_length=2),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[ClinicalCase]:
    query = select(ClinicalCase).options(selectinload(ClinicalCase.created_by)).order_by(ClinicalCase.created_at.desc())
    if status_filter:
        query = query.where(ClinicalCase.status == status_filter)
    if search:
        query = query.where(ClinicalCase.title.ilike(f"%{search}%"))
    return list(db.scalars(query.limit(limit).offset(offset)).all())


@router.get("/{case_id}", response_model=CaseRead)
def get_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ClinicalCase:
    case = db.scalar(
        select(ClinicalCase)
        .options(selectinload(ClinicalCase.created_by))
        .where(ClinicalCase.id == case_id)
    )
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.patch("/{case_id}", response_model=CaseRead)
def update_case(
    case_id: int,
    payload: CaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ClinicalCase:
    case = db.get(ClinicalCase, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    data = payload.model_dump(exclude_unset=True)
    old_status = case.status

    for field, value in data.items():
        setattr(case, field, value)

    if "status" in data and data["status"] != old_status:
        db.add(StatusHistory(case_id=case.id, old_status=old_status, new_status=case.status, changed_by_id=current_user.id))

    db.commit()
    db.refresh(case)
    return db.scalar(
        select(ClinicalCase)
        .options(selectinload(ClinicalCase.created_by))
        .where(ClinicalCase.id == case.id)
    )


@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    case = db.get(ClinicalCase, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    db.delete(case)
    db.commit()


@router.get("/{case_id}/status-history", response_model=list[StatusHistoryRead])
def get_status_history(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[StatusHistory]:
    case = db.get(ClinicalCase, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return list(db.scalars(select(StatusHistory).where(StatusHistory.case_id == case_id).order_by(StatusHistory.changed_at)).all())
