from enum import Enum
from typing import List, TypeVar, Generic

from model.models import DbUser, DbPost, DbComment
from pydantic import BaseModel, EmailStr

T = TypeVar("T");


class Pagination(BaseModel, Generic[T]):
    total: int
    page: int
    per_page: int
    data: List[T]


class UserType(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    REGULAR = "REGULAR"


class RegisterParams(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    type: UserType


class UserUpdate(BaseModel):
    username: str
    email: EmailStr


class User(BaseModel):
    id: int
    uid: str
    username: str
    email: str
    type: UserType


class PostCreate(BaseModel):
    image_url: str
    title: str


class Post(BaseModel):
    id: int
    uid: str
    image_url: str
    title: str
    timestamp: str
    user_id: int


class CommentCreate(BaseModel):
    text: str


class Comment(BaseModel):
    id: int
    uid: str
    text: str
    user_id: int
    timestamp: str
    post_id: int


def convert_user_model(user: DbUser):
    return {
        "id": user.id,
        "uid": user.uid,
        "username": user.username,
        "email": user.email,
        "type": user.type
    }


def convert_full_user(user: DbUser):
    return {
        "id": user.id,
        "uid": user.uid,
        "username": user.username,
        "email": user.email,
        "type": user.type
    } if user else None


def convert_post(post: DbPost):
    return {
        "id": post.id,
        "uid": post.uid,
        "title": post.title,
        "image_url": post.image_url,
        "timestamp": str(post.timestamp),
        "user_id": post.user_id
    } if post else None


def convert_comment(comment: DbComment):
    return {
        "id": comment.id,
        "uid": comment.uid,
        "text": comment.text,
        "timestamp": str(comment.timestamp),
        "user_id": comment.user_id,
        "post_id": comment.post_id
    } if comment else None
