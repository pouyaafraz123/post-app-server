from typing import Optional

from authentication.oauth2 import get_current_user
from controller import comment
from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schema.schemas import Comment, User, CommentCreate, Pagination, UserType
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/comment',
    tags=['comment']
)


@router.post("/{post_id}", response_model=Comment)
def create_comment(
        post_id: int,
        request: CommentCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return comment.create_comment(db, request, current_user.id, post_id)


@router.get("", response_model=Pagination[Comment])
def get_comments(
        page: Optional[int] = 1,
        per_page: Optional[int] = 10,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return comment.get_comments(db, page, per_page)


@router.get("/{comment_id}", response_model=Comment)
def get_comment(comment_id: int, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    c = comment.get_comment(db, comment_id)
    if c is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Comment Not Found")
    return c


@router.put('/{comment_id}', response_model=Comment, summary="Update Post")
def update_comment(
        comment_id: int,
        request: CommentCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    c = comment.get_comment(db, comment_id)

    if c is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="comment not found")
    if current_user.type != UserType.SUPER_ADMIN and c.user_id != \
            current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="user does not have right permission")
    return comment.update_comment(db, request, comment_id)


@router.delete('/{comment_id}', response_model=int, summary="Delete Comment")
def delete_comment(
        comment_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    c = comment.get_comment(db, comment_id)

    if c is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="comment not found")
    if current_user.type != UserType.SUPER_ADMIN and c.user_id != \
            current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="user does not have right permission")
    return comment.delete_comment(db, comment_id)
