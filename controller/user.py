from uuid import uuid4

from controller.hashing import Hash
from model.models import DbUser, DbPost, DbComment
from schema.schemas \
    import UserCreate, \
    convert_user_model, \
    convert_full_user, \
    UserUpdate, \
    RegisterParams, \
    UserType
from sqlalchemy.orm.session import Session


def create_user(db: Session, request: UserCreate):
    data = RegisterParams(
        email=request.email,
        username=request.username,
        password=request.password)
    return create(db, data, request.type)


def register_user(db: Session, request: RegisterParams):
    return create(db, request, UserType.REGULAR)


def create(db: Session, request: RegisterParams, user_type: UserType):
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password),
        uid="USER_" + str(uuid4()),
        type=user_type
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return convert_user_model(new_user)


def get_all(db: Session):
    users = db.query(DbUser).all()
    return list(map(lambda user: convert_user_model(user), users))


def get_users(db: Session, page: int, per_page: int):
    count = db.query(DbUser).count()
    users = db.query(DbUser).order_by(DbUser.id.desc()).limit(
        per_page).offset((page - 1) * per_page).all()
    return {
        "page": page,
        "per_page": per_page,
        "total": count,
        "data": list(map(lambda user: convert_user_model(user), users))
    }


def get_user(db: Session, user_id: int):
    user = db.query(DbUser).get(user_id)
    return convert_full_user(user)


def update_user(db: Session, user_id: int, request: UserUpdate):
    user_id = db.query(DbUser).filter(DbUser.id == user_id).update(values={
        "username": request.username,
        "email": request.email,
    })
    db.commit()
    return convert_full_user(db.query(DbUser).get(user_id))


def promote_user(db: Session, user_id: int):
    user_id = db.query(DbUser).filter(DbUser.id == user_id).update(values={
        "type": UserType.SUPER_ADMIN
    })
    db.commit()
    return convert_full_user(db.query(DbUser).get(user_id))


def delete_user(db: Session, user_id: int):
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    db.delete(user)
    posts = db.query(DbPost).filter(DbPost.user_id == user_id).all()
    for post in posts:
        db.query(DbComment).filter(DbComment.post_id == post.id).delete()
    db.query(DbComment).filter(DbComment.user_id == user_id).delete()
    db.query(DbPost).filter(DbPost.user_id == user_id).delete()
    db.commit()
    return user.id


def user_exist_with_id(db: Session, user_id: int):
    user = db.query(DbUser).get(user_id)
    if user is None:
        return False
    return True


def get_user_with_username(db: Session, username: str):
    return db.query(DbUser).filter(DbUser.username == username).first()


def get_user_with_email(db: Session, email: str):
    return db.query(DbUser).filter(DbUser.email == email).first()


def user_exist_with_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if user is None:
        return False
    return True


def user_exist_with_email(db: Session, email: str):
    user = db.query(DbUser).filter(DbUser.email == email).first()
    if user is None:
        return False
    return True
