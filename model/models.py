import datetime

from database.database import Base
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey


class DbUser(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True,
                                    autoincrement=True)
    uid: Mapped[str] = mapped_column(String, unique=True, index=True,
                                     nullable=False)
    type: Mapped[String] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)


class DbPost(Base):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True,
                                    autoincrement=True)
    uid: Mapped[str] = mapped_column(String, unique=True, index=True,
                                     nullable=False)
    image_url: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'),
                                         index=True)


class DbComment(Base):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True,
                                    autoincrement=True)
    uid: Mapped[str] = mapped_column(String, unique=True, index=True,
                                     nullable=False)
    text: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'))
