from uuid import uuid4

from model.models import DbPost
from schema.schemas import PostCreate, convert_post
from sqlalchemy.orm import Session


def create_post(db: Session, request: PostCreate, user_id: int):
    new_post = DbPost(
        uid="POST_" + str(uuid4()),
        image_url=request.image_url,
        title=request.title,
        user_id=user_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return convert_post(new_post)


def get_all(db: Session):
    posts = db.query(DbPost).all()
    return list(map(lambda post: convert_post(post), posts))


def get_posts(db: Session, page: int, per_page: int):
    count = db.query(DbPost).count()
    posts = db.query(DbPost).order_by(DbPost.timestamp.desc()).limit(
        per_page).offset((page - 1) * per_page).all()
    return {
        "page": page,
        "per_page": per_page,
        "total": count,
        "data": list(map(lambda post: convert_post(post), posts))
    }


def get_user_posts(db: Session, page: int, per_page: int, user_id: int):
    count = db.query(DbPost).filter(DbPost.user_id == user_id).count()
    posts = db.query(DbPost).order_by(DbPost.timestamp.desc()).filter(
        DbPost.user_id == user_id).limit(
        per_page).offset((page - 1) * per_page
                         ).all()
    return {
        "page": page,
        "per_page": per_page,
        "total": count,
        "data": list(map(lambda post: convert_post(post), posts))
    }


def get_post(db: Session, post_id: int):
    return convert_post(db.query(DbPost).get(post_id))


def is_post_exist(db: Session, id: int):
    if get_post(db, id) is None:
        return False
    return True


def update_post(db: Session, request: PostCreate, post_id: int):
    post_id = db.query(DbPost).filter(DbPost.id == post_id).update(values={
        "title": request.title,
        "image_url": request.image_url,
    })
    return convert_post(db.query(DbPost).get(post_id))


def delete_post(db: Session, post_id: int):
    post = db.query(DbPost).filter(DbPost.id == post_id).first()
    db.delete(post)
    db.commit()
    return post_id
