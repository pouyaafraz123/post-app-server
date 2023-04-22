from uuid import uuid4

from model.models import DbComment
from schema.schemas import CommentCreate, convert_comment
from sqlalchemy.orm import Session


def create_comment(
        db: Session,
        request: CommentCreate,
        user_id: int,
        post_id: int):
    new_comment = DbComment(
        uid="COMMENT_" + str(uuid4()),
        text=request.text,
        user_id=user_id,
        post_id=post_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return convert_comment(new_comment)


def get_comments(db: Session, page: int, per_page: int):
    count = db.query(DbComment).count()
    comments = db.query(DbComment).order_by(DbComment.timestamp.desc()).limit(
        per_page).offset((page - 1) *
                         per_page).all()
    return {
        "page": page,
        "per_page": per_page,
        "total": count,
        "data": list(map(lambda comment: convert_comment(comment), comments))
    }


def get_user_comments(db: Session, page: int, per_page: int, user_id: int):
    count = db.query(DbComment).filter(DbComment.user_id == user_id).count()
    comments = db.query(DbComment).filter(
        DbComment.user_id == user_id).order_by(
        DbComment.timestamp.desc()).limit(
        per_page).offset((page - 1) * per_page
                         ).all()
    return {
        "page": page,
        "per_page": per_page,
        "total": count,
        "data": list(map(lambda comment: convert_comment(comment), comments))
    }


def get_post_comments(db: Session, page: int, per_page: int, post_id: int):
    count = db.query(DbComment).filter(DbComment.post_id == post_id).count()
    comments = db.query(DbComment).filter(
        DbComment.post_id == post_id).order_by(
        DbComment.timestamp.desc()).limit(
        per_page).offset((page - 1) * per_page
                         ).all()
    return {
        "page": page,
        "per_page": per_page,
        "total": count,
        "data": list(map(lambda comment: convert_comment(comment), comments))
    }


def get_comment(db: Session, comment_id: int):
    return convert_comment(db.query(DbComment).get(comment_id))


def is_comment_exist(db: Session, id: int):
    if get_comment(db, id) is None:
        return False
    return True


def update_comment(db: Session, request: CommentCreate, comment_id: int):
    comment_id = db.query(DbComment).filter(DbComment.id == comment_id).update(
        values={
            "text": request.text,
        })
    return convert_comment(db.query(DbComment).get(comment_id))


def delete_comment(db: Session, comment_id: int):
    print(comment_id)
    comment = db.query(DbComment).filter(DbComment.id == comment_id).first()
    db.delete(comment)
    db.commit()
    return comment_id
