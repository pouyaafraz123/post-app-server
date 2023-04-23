import random
import shutil
import string
from typing import Optional

from authentication.oauth2 import get_current_user
from controller import post, comment
from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from schema.schemas import Post, PostCreate, User, Pagination, UserType, Comment
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/post',
    tags=['post']
)


@router.post("", response_model=Post)
def create_post(
        request: PostCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return post.create_post(db, request, current_user.id)


@router.get("", response_model=Pagination[Post])
def get_posts(
        page: Optional[int] = 1,
        per_page: Optional[int] = 10,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return post.get_posts(db, page, per_page)


@router.get("/{post_id}", response_model=Post)
def get_post(post_id: int, db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):
    p = post.get_post(db, post_id)
    if p is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post Not Found")
    return p


@router.put('/{post_id}', response_model=Post, summary="Update Post")
def update_post(
        post_id: int,
        request: PostCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    p = post.get_post(db, post_id)

    if p is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post not found")
    if current_user.type != UserType.SUPER_ADMIN and \
            p["user_id"] != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="user does not have right permission")
    return post.update_post(db, request, post_id)


@router.delete('/{post_id}', response_model=int, summary="Delete Post")
def delete_post(
        post_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    p = post.get_post(db, post_id)

    if p is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post not found")
    if current_user.type != UserType.SUPER_ADMIN and p["user_id"] != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="user does not have right permission")
    return post.delete_post(db, post_id)


@router.post('/image')
def upload_image(image: UploadFile = File(...)):
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'filename': path}


@router.get("/{post_id}/comments", response_model=Pagination[Comment], )
def get_post_comments(
        post_id: int,
        page: Optional[int] = 1,
        per_page: Optional[int] = 10,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return comment.get_post_comments(db, page, per_page, post_id)
