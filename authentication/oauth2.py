from datetime import datetime, timedelta
from typing import Optional

from controller import user as USER
from database.database import get_db
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from schema.schemas import UserType
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = '333809dfe79d55fc49216952965632e7cc0b46b1d27ce34792581014a6cef1b1c0231d2cf2f49241a0e2a56878f9bb52f6b98e6c71ec8e5d25db5ab6be5eb33e2d1068b6479d3b01f904cf057fc7b8648d5db6f5ab6b5ca6d532205d9a9a38ebf91301f10bc39935f8b1d9772f2c10122c659d7e61c6941f2a262f14eb0c4a0d4d4e21207d24d60c21dd861d8b9c9e7f684135a25da2e38cc94a0d0a3efb84469c63d61749dd9c9fcfae2f32b50ed63b4d4b4f1c7c4574a1f88a9d9c14ef83b9da6745482cc2e853ce89a3f5227ca1b29d8b4142719b94e6183b3a20a69e55b7266d0f0b5ab6b5caa6d531e9c9fc1ae2f32b50ed63b4d4b4f1c7c4574a1f88a9d9c14ef83b9da6745482cc2e853ce89a3f5227ca1b29d8b4142719b94e6183b3a20a69e55b7266d0f0b5ab6b5caa6d531e9c9fc1ae2f32b50ed63b4d4b4f1c7c4574a1f88a9d9c14ef83b9da6745482cc2e853ce89a3f5227ca1b29d8b4142719b94e6183b3a20a69e55b7266d0f0b5ab6b5caa6d531e9c9fc1ae2f32b50ed63b4d4b4f1c7c4574a1f88a9d9c14ef83b9da6745482cc2e853ce89a3f5227ca1b29d8b4142719b94e6183b3a20a69e55b7266d0f0b5ab6b5caa6d531e9c9fc1ae2f32b50ed63b4d4b4f1c7c4574a1f88a9d9c14ef83b9da6745482cc2e853ce89a3f5227ca1b29d8b4142719b94e6183b3a20a69e55b7266d0f0b5ab6b5caa6d531e9c9fc1ae2f32b50ed63b4d4b4f1c7c4574a1f88a9d9c14ef83b9da6745482cc2e853ce89a3f5227ca1b29d8b4142719b94e6183b3a20a69e55b7266d0f0b5ab6b5caa6d531'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60000


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = USER.get_user_with_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


def get_admin_user(token: str = Depends(oauth2_scheme),
                   db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Un Authorized Access",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = USER.get_user_with_username(db, username=username)
    if user is None:
        raise credentials_exception
    if user.type != UserType.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
