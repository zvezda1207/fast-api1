from sqlalchemy import Boolean, DateTime, Integer, String, UUID, ForeignKey, func, text
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker, create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

import config
from custom_type import ROLE
import uuid
import datetime

engine = create_async_engine(config.PG_DSN)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    @property
    def id_dict(self):
        return {'id': self.id}

class Token(Base):
    __tablename__ = 'token'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(UUID, unique=True, server_default=func.gen_random_uuid())
    creation_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship('User', lazy='joined', back_populates='tokens')

    @property
    def dict(self):
        return {'token': self.token}

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    role: Mapped[ROLE] = mapped_column(String, default='user')
    tokens: Mapped[list['Token']] = relationship('Token', lazy='joined', back_populates='user')
    todos: Mapped[list['Todo']] = relationship('Todo', lazy='joined', back_populates='user')
    
    @property
    def dict(self):
        return {'id': self.id, 'name': self.name, 'role': self.role}

class Todo(Base):
    __tablename__ = 'todo'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True)
    important: Mapped[bool] = mapped_column(Boolean, default=False)
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    end_time: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship('User', lazy='joined', back_populates='todos')

    @property
    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'done': self.done,
            'important': self.important, 
            'start_time': self.start_time.isoformat(),
            'end_time': (self.end_time.isoformat() if self.end_time is not None else None),
            'user_id': self.user_id,
        }

ORM_OBJ = Todo | User | Token
ORM_CLS = type[Todo] | type[User] | type[Token]

async def init_orm():
    async with engine.begin() as conn:
        # await conn.execute(text('TRUNCATE TABLE token, "user", todo RESTART IDENTITY CASCADE;'))
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()