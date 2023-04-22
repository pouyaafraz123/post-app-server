from authentication.oauth2 import create_access_token, get_current_user
from controller import user
from controller.hashing import Hash
from controller.user import register_user
from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from model.models import DbUser
from schema.schemas import RegisterParams, User, convert_full_user
from sqlalchemy.orm.session import Session

router = APIRouter(
    tags=['authentication']
)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid credentials')
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Incorrect password')

    access_token = create_access_token(data={'username': user.username})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username,
        'type': user.type
    }


@router.post('/register', response_model=User)
def register(request: RegisterParams, db: Session = Depends(get_db)):
    if user.user_exist_with_username(db, request.username):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="username exist")
    if user.user_exist_with_email(db, request.email):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="email exist")
    return register_user(db, request)


@router.get("/profile", response_model=User)
def getProfile(current_user: User = Depends(get_current_user),
               db: Session = Depends(
                   get_db)):
    return convert_full_user(current_user)
