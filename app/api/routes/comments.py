from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.case import ClinicalCase
from app.models.comment import Comment
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentRead

router = APIRouter(prefix="/cases/{case_id}/comments", tags=["comments"])


@router.post("", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(
    case_id: int,
    payload: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Comment:
    if not db.get(ClinicalCase, case_id):
        raise HTTPException(status_code=404, detail="Case not found")

    comment = Comment(case_id=case_id, author_id=current_user.id, text=payload.text)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return db.scalar(select(Comment).options(selectinload(Comment.author)).where(Comment.id == comment.id))


@router.get("", response_model=list[CommentRead])
def list_comments(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Comment]:
    if not db.get(ClinicalCase, case_id):
        raise HTTPException(status_code=404, detail="Case not found")

    return list(
        db.scalars(
            select(Comment)
            .options(selectinload(Comment.author))
            .where(Comment.case_id == case_id)
            .order_by(Comment.created_at)
        ).all()
    )
