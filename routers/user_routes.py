from typing import Optional

from authentication.oauth2 import get_admin_user, get_current_user
from controller import user, post, comment
from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schema.schemas import UserCreate, Pagination, User, UserUpdate, Post, \
    UserType, Comment
from sqlalchemy.orm.session import Session

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('', response_model=User, summary="Create User")
def create_user(
        request: UserCreate,
        db: Session = Depends(get_db),
        admin_user: User = Depends(get_admin_user)
):
    if user.user_exist_with_username(db, request.username):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="username exist")
    if user.user_exist_with_email(db, request.email):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="email exist")
    return user.create_user(db, request)


@router.get('', response_model=Pagination[User], summary="Get All Users")
def get_all_users(
        page: Optional[int] = 1,
        per_page: Optional[int] = 10,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return user.get_users(db, page, per_page)


@router.get('/{user_id}', response_model=User, summary="Get User")
def get_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    u = user.get_user(db, user_id)
    if u is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user not found")
    return u


@router.put('/promote/{user_id}', response_model=User, summary="Promote User")
def promote_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    u = user.get_user(db, user_id)
    if u is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user not found")
    if current_user.type != UserType.SUPER_ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="user does not have right permission")
    return user.promote_user(db, user_id)


@router.put('/{user_id}', response_model=User, summary="Update User")
def update_user(
        user_id: int,
        request: UserUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    u = user.get_user(db, user_id)
    if u is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user not found")
    if current_user.type != UserType.SUPER_ADMIN and user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="user does not have right permission")
    if user.user_exist_with_username(db, request.username):
        if user.get_user_with_username(db, request.username).id != user_id:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="username already exist")
    if user.user_exist_with_email(db, request.email):
        if user.get_user_with_email(db, request.email).id != user_id:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="email already exist")
    return user.update_user(db, user_id, request)


@router.delete('/{user_id}', response_model=int, summary="Delete User")
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    u = user.get_user(db, user_id)
    if u is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user not found")
    if current_user.type != UserType.SUPER_ADMIN and user_id != \
            current_user.id or u["type"] == UserType.SUPER_ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="user does not have right permission")
    return user.delete_user(db, user_id)


@router.get("/{user_id}/posts", response_model=Pagination[Post],
            summary="Get User's Posts")
def get_user_posts(user_id: int, page: Optional[int] = 1,
                   per_page: Optional[int] = 10, db: Session = Depends(
            get_db), current_user: User = Depends(get_current_user)):
    if not user.user_exist_with_id(db, user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user not found")
    return post.get_user_posts(db, page, per_page, user_id)


@router.get("/{user_id}/comments", response_model=Pagination[Comment])
def get_user_comments(
        user_id: int,
        page: Optional[int] = 1,
        per_page: Optional[int] = 10,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return comment.get_user_comments(db, page, per_page, user_id)
